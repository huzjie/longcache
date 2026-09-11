"""TopK 选择器：稀疏注意力里「每个查询只关注最重要的 k 个键」的核心算子。

对应 DeepSelect 加速的 TopK。纯 Python 实现用堆 + 部分选择逼近，避免 O(n log n)
全排序，复杂度 O(n log k)。
"""
from __future__ import annotations

import heapq
from typing import List, Tuple


class TopKSelector:
    """从一批 (key_id, score) 里选出分数最高的 k 个，返回 key_id 列表。

    使用最小堆维护「当前最大的 k 个」，遍历一次即完成，时间复杂度 O(n log k)、
    空间 O(k)。相比 `sorted(..., reverse=True)[:k]` 的 O(n log n) 更高效，
    也是 DeepSelect 在 GPU 上以定制 kernel 加速的算法内核。
    """

    def __init__(self, k: int):
        if k <= 0:
            raise ValueError("k 必须为正整数")
        self.k = k

    def select(self, pairs: List[Tuple[int, float]]) -> List[int]:
        """pairs: [(key_id, score), ...]，返回分数最高的 k 个 key_id（降序）。"""
        if len(pairs) <= self.k:
            return [kid for kid, _ in pairs]
        heap: List[Tuple[float, int]] = []
        for kid, score in pairs:
            if len(heap) < self.k:
                heapq.heappush(heap, (score, kid))
            elif score > heap[0][0]:
                heapq.heapreplace(heap, (score, kid))
        top = sorted(heap, key=lambda x: -x[0])
        return [kid for _, kid in top]

    def select_scores(self, pairs: List[Tuple[int, float]]) -> List[Tuple[int, float]]:
        """同 select，但额外返回 (key_id, score)。"""
        ids = set(self.select(pairs))
        return [(kid, s) for kid, s in pairs if kid in ids]


def topk_scores(scores: List[float], k: int) -> List[int]:
    """便捷函数：给定分数列表，返回 top-k 的下标。"""
    sel = TopKSelector(k)
    return sel.select(list(enumerate(scores)))
