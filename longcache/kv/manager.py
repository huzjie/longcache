"""KV 管理器：把预算/量化/压缩/驱逐/滑动窗口串成完整生命周期。"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from longcache.config.schema import KVConfig
from longcache.core.errors import KVError
from longcache.core.utils import stable_hash
from longcache.kv.block import KVBlock
from longcache.kv.budget import MemoryBudget, estimate_bytes_per_token
from longcache.kv.compression import get_compressor
from longcache.kv.eviction import get_eviction
from longcache.kv.quant import get_quantizer
from longcache.models.spec import ModelSpec


@dataclass
class KVStats:
    """KV 运行统计。"""
    writes: int = 0
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    blocks_used: int = 0


class KVManager:
    """统一管理 KV Cache。

    核心流程：
    1. 按模型结构 + 量化位宽估算每 token 字节数，建立内存预算；
    2. 写入 token 时生成块（含指纹），超预算则按驱逐策略淘汰；
    3. 命中查询走指纹索引；
    4. 可选压缩（TopK/池化/采样）进一步降低驻留。
    """

    def __init__(self, cfg: KVConfig, model: Optional[ModelSpec] = None):
        self.cfg = cfg
        self.model = model
        # 每 token 字节数：优先用模型卡标称值，否则按结构估算
        if model is not None and model.kv_cache_bytes_per_token > 0:
            per_token = model.kv_cache_bytes_per_token
        else:
            width = get_quantizer(cfg.quant).bytes_per_value
            heads_kv = model.heads_kv if model else 64
            layers = model.layers if model else 40
            head_dim = 128
            per_token = estimate_bytes_per_token(width, heads_kv, layers, head_dim)
        self.per_token_bytes = per_token
        self.budget = MemoryBudget(cfg.budget_bytes, per_token, cfg.block_size)
        self.compressor = get_compressor(cfg.compression)
        self.evictor = get_eviction(cfg.eviction)

        self._blocks: Dict[int, KVBlock] = {}
        self._fingerprint_index: Dict[int, List[int]] = {}
        self._next_id = 0
        self._clock = 0.0
        self.stats = KVStats()

    # -- 写入 ----------------------------------------------------------------
    def write(self, seq_id: int, start_pos: int, text: str) -> List[int]:
        """为一个序列写入一段文本对应的 KV 块，返回写入的块 id 列表。"""
        tokens = max(1, len(text))
        n_blocks = (tokens + self.cfg.block_size - 1) // self.cfg.block_size
        written: List[int] = []
        for i in range(n_blocks):
            bid = self._allocate(seq_id, start_pos + i * self.cfg.block_size,
                                 text[i * self.cfg.block_size:(i + 1) * self.cfg.block_size])
            written.append(bid)
        self.stats.writes += 1
        return written

    def _allocate(self, seq_id: int, pos: int, chunk: str) -> int:
        fp = stable_hash(chunk, 32)
        # 命中已存在块则直接复用
        if fp in self._fingerprint_index:
            for bid in self._fingerprint_index[fp]:
                self._blocks[bid].touch(self._clock)
                self.stats.hits += 1
                return bid

        self._clock += 1.0
        # 驱逐到预算以内
        while (self.current_bytes() + self._block_nbytes() > self.cfg.budget_bytes
               and self._blocks):
            self._evict_one()

        bid = self._next_id
        self._next_id += 1
        blk = KVBlock(block_id=bid, seq_id=seq_id, start_pos=pos,
                      block_size=self.cfg.block_size, fingerprint=fp,
                      nbytes=self._block_nbytes(), last_access=self._clock)
        self._blocks[bid] = blk
        self._fingerprint_index.setdefault(fp, []).append(bid)
        self.stats.misses += 1
        self.stats.blocks_used = len(self._blocks)
        return bid

    def _block_nbytes(self) -> int:
        return max(1, self.cfg.block_size * int(self.per_token_bytes))

    def _evict_one(self) -> None:
        victim = self.evictor.select_victim(list(self._blocks.values()))
        if victim is None:
            return
        self._blocks.pop(victim.block_id, None)
        lst = self._fingerprint_index.get(victim.fingerprint, [])
        if victim.block_id in lst:
            lst.remove(victim.block_id)
        if not lst:
            self._fingerprint_index.pop(victim.fingerprint, None)
        self.stats.evictions += 1
        self.stats.blocks_used = len(self._blocks)

    # -- 查询 ----------------------------------------------------------------
    def lookup(self, text: str) -> bool:
        """判断一段文本是否命中缓存（指纹索引）。"""
        fp = stable_hash(text, 32)
        if fp in self._fingerprint_index:
            for bid in self._fingerprint_index[fp]:
                self._blocks[bid].touch(self._clock)
            self.stats.hits += 1
            return True
        self.stats.misses += 1
        return False

    def compress_context(self, total_tokens: int) -> List[int]:
        """对超长上下文做压缩，返回保留位置。"""
        if self.cfg.hybrid:
            from longcache.kv.hybrid import HybridCache
            hc = HybridCache(self.cfg.sliding_window or 1024, self.cfg.compression_ratio)
            hc.update(total_tokens, self.compressor)
            return hc.kept_positions()
        if self.cfg.sliding_window > 0:
            from longcache.kv.sliding import SlidingWindow
            sw = SlidingWindow(self.cfg.sliding_window)
            for p in range(total_tokens):
                sw.push(p)
            return sw.positions
        return self.compressor.select(total_tokens, self.cfg.compression_ratio)

    # -- 统计 ----------------------------------------------------------------
    def current_bytes(self) -> int:
        return sum(b.nbytes for b in self._blocks.values())

    def hit_rate(self) -> float:
        total = self.stats.hits + self.stats.misses
        return self.stats.hits / total if total else 0.0

    def effective_ratio(self) -> float:
        """有效压缩比：FP16（每值 2 字节）相对当前量化位宽的倍数。

        FP4（0.5B）→ 4x；FP8/INT8（1B）→ 2x；none（2B）→ 1x。
        """
        from longcache.kv.quant import get_quantizer
        width = get_quantizer(self.cfg.quant).bytes_per_value
        return 2.0 / width if width else 1.0

    def describe(self) -> Dict:
        return {
            "budget_bytes": self.cfg.budget_bytes,
            "per_token_bytes": self.per_token_bytes,
            "max_tokens": self.budget.max_tokens,
            "blocks": len(self._blocks),
            "current_bytes": self.current_bytes(),
            "hit_rate": self.hit_rate(),
            "evictions": self.stats.evictions,
            "compression_ratio": self.effective_ratio(),
        }
