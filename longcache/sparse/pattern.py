"""稀疏注意力模式：local / sliding / global / block（可插拔注册表）。"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from longcache.core.registry import Registry

SparsePatternRegistry = Registry("sparse_pattern")


class SparsePattern(ABC):
    """稀疏模式抽象：给定序列长度与查询位置，返回该查询允许关注的键位置集合。"""

    name: str = "base"

    @abstractmethod
    def allowed_keys(self, seq_len: int, query_pos: int, window: int) -> List[int]:
        """返回 query_pos 允许关注的键位置列表（升序）。"""


@SparsePatternRegistry.register("local")
class LocalPattern(SparsePattern):
    """局部模式：只关注当前窗口内的键。"""

    name = "local"

    def allowed_keys(self, seq_len: int, query_pos: int, window: int) -> List[int]:
        lo = max(0, query_pos - window)
        hi = min(seq_len, query_pos + window + 1)
        return list(range(lo, hi))


@SparsePatternRegistry.register("sliding")
class SlidingPattern(SparsePattern):
    """滑动窗口：关注当前位置往前的 window 个键（因果）。"""

    name = "sliding"

    def allowed_keys(self, seq_len: int, query_pos: int, window: int) -> List[int]:
        lo = max(0, query_pos - window)
        return list(range(lo, query_pos + 1))


@SparsePatternRegistry.register("global")
class GlobalPattern(SparsePattern):
    """全局模式：全量关注（退化为 dense）。"""

    name = "global"

    def allowed_keys(self, seq_len: int, query_pos: int, window: int) -> List[int]:
        return list(range(seq_len))


@SparsePatternRegistry.register("topk")
class TopKPattern(SparsePattern):
    """TopK 模式：全局候选 + TopK 收缩（DeepSelect 主打策略）。

    返回全量键作为候选，随后由 TopKSelector 收缩到最重要的 k 个，
    实现 O(n log k) 的稀疏注意力。
    """

    name = "topk"

    def allowed_keys(self, seq_len: int, query_pos: int, window: int) -> List[int]:
        return list(range(seq_len))


@SparsePatternRegistry.register("block")
class BlockPattern(SparsePattern):
    """块稀疏：按 block 划分，只关注与当前块相邻的若干块。"""

    name = "block"

    def allowed_keys(self, seq_len: int, query_pos: int, window: int) -> List[int]:
        block = window if window > 0 else 128
        cur = query_pos // block
        keys = []
        for b in range(max(0, cur - 1), cur + 2):
            lo = b * block
            hi = min(seq_len, (b + 1) * block)
            keys.extend(range(lo, hi))
        return keys


def get_pattern(name: str) -> SparsePattern:
    try:
        return SparsePatternRegistry.get(name)()
    except KeyError:
        raise ValueError(f"未知稀疏模式 {name!r}，可用：{SparsePatternRegistry.keys()}")
