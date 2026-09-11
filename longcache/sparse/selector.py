"""稀疏注意力选择器：把策略/模式/索引统一成一个门面。"""
from __future__ import annotations

from typing import List, Tuple

from longcache.config.schema import SparseConfig
from longcache.sparse.topk import TopKSelector
from longcache.sparse.pattern import get_pattern
from longcache.sparse.index import StreamingIndex, HierarchicalIndex
from longcache.core.utils import stable_hash


def _mock_score(key_id: int, query_id: int) -> float:
    """确定性 mock 注意力分数（真实实现为 Q·K^T）。"""
    return float((key_id * 2654435761 + query_id * 40503) & 0xFFFF) / 65535.0


class SparseSelector:
    """根据配置选择稀疏注意力策略并执行选择。"""

    def __init__(self, cfg: SparseConfig):
        self.cfg = cfg
        self.pattern = get_pattern(cfg.strategy)
        self.topk = TopKSelector(cfg.topk)

    def select(self, seq_len: int, query_pos: int) -> List[int]:
        """返回 query_pos 允许关注的键位置（稀疏化后）。"""
        # 先按模式拿到候选集
        candidates = self.pattern.allowed_keys(seq_len, query_pos, self.cfg.local_window)
        # 若候选过大，用 TopK 进一步收缩（DeepSelect）
        if len(candidates) > self.cfg.topk:
            pairs = [(kid, _mock_score(kid, query_pos)) for kid in candidates]
            return self.topk.select(pairs)
        return candidates

    def build_index(self, token_ids: List[int]) -> StreamingIndex:
        """为一批 token 建立流感知索引。"""
        idx = StreamingIndex(topk=self.cfg.topk)
        for t in token_ids:
            idx.ingest(t, float(stable_hash(str(t), 16)) / 65535.0)
        return idx

    def describe(self) -> dict:
        return {
            "strategy": self.cfg.strategy,
            "topk": self.cfg.topk,
            "local_window": self.cfg.local_window,
            "index": self.cfg.index,
        }
