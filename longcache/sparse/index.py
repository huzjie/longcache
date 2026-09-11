"""稀疏注意力索引：流感知 / 跨层 / 层级化三种索引结构。

对应 DeepSeek LongCat 稀疏注意力的「流感知索引、跨层索引、层级化索引」三项策略，
用于在长上下文中快速定位候选键，减少碎片化访存与重复索引计算。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set

from longcache.core.utils import stable_hash


@dataclass
class StreamingIndex:
    """流感知索引：按 token 流维护「高分 token」的增量索引，边流边选。"""
    topk: int = 256
    _scores: Dict[int, float] = field(default_factory=dict)

    def ingest(self, token_id: int, score: float) -> None:
        self._scores[token_id] = max(self._scores.get(token_id, 0.0), score)

    def top_positions(self) -> List[int]:
        if len(self._scores) <= self.topk:
            return sorted(self._scores)
        ranked = sorted(self._scores.items(), key=lambda x: -x[1])
        return sorted(k for k, _ in ranked[:self.topk])


@dataclass
class CrossLayerIndex:
    """跨层索引：不同层共享同一份候选键索引，避免逐层重复计算。"""
    _candidates: List[int] = field(default_factory=list)

    def build(self, positions: List[int]) -> None:
        self._candidates = positions

    def for_layer(self, layer_id: int) -> List[int]:
        # 跨层复用，不同层可做轻微扰动（确定性）
        return self._candidates


@dataclass
class HierarchicalIndex:
    """层级化索引：先粗粒度（块级）后细粒度（token 级）两级检索。"""
    block_size: int = 64
    _block_scores: Dict[int, float] = field(default_factory=dict)

    def ingest(self, token_id: int, score: float) -> None:
        b = token_id // self.block_size
        self._block_scores[b] = max(self._block_scores.get(b, 0.0), score)

    def top_blocks(self, k: int) -> List[int]:
        ranked = sorted(self._block_scores.items(), key=lambda x: -x[1])
        return [b for b, _ in ranked[:k]]

    def expand(self, block_ids: List[int], seq_len: int) -> List[int]:
        """把块号展开成 token 位置。"""
        pos: Set[int] = set()
        for b in block_ids:
            lo = b * self.block_size
            hi = min(seq_len, (b + 1) * self.block_size)
            pos.update(range(lo, hi))
        return sorted(pos)
