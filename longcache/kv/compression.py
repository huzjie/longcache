"""KV 压缩策略：TopK / 平均池化 / 采样（用于超长上下文降内存）。"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from longcache.core.registry import Registry
from longcache.core.errors import KVError

CompressionRegistry = Registry("compression")


@dataclass
class CompressResult:
    """压缩结果：保留的 token 位置 + 压缩比。"""
    kept_positions: List[int]
    ratio: float


class Compressor(ABC):
    """KV 压缩器抽象：给定 token 数与原序列长度，返回保留位置。"""

    @abstractmethod
    def select(self, total: int, ratio: float) -> List[int]:
        """返回保留的 token 下标（升序）。ratio 为目标保留比例。"""


@CompressionRegistry.register("none")
class NoCompress(Compressor):
    """不压缩，全保留。"""

    def select(self, total: int, ratio: float) -> List[int]:
        return list(range(total))


@CompressionRegistry.register("topk")
class TopKCompress(Compressor):
    """TopK：保留「重要度最高」的 k 个 token（这里用确定性哈希模拟重要度评分，
    真实实现中由注意力分数驱动）。"""

    def select(self, total: int, ratio: float) -> List[int]:
        k = max(1, int(total * ratio))
        if k >= total:
            return list(range(total))
        # 用哈希模拟重要性，选择哈希值最大的 k 个位置
        scored = [(i, (i * 2654435761) & 0xFFFFFFFF) for i in range(total)]
        scored.sort(key=lambda x: -x[1])
        return sorted(i for i, _ in scored[:k])


@CompressionRegistry.register("avgpool")
class AvgPoolCompress(Compressor):
    """平均池化：等间距采样。"""

    def select(self, total: int, ratio: float) -> List[int]:
        k = max(1, int(total * ratio))
        if k >= total:
            return list(range(total))
        step = total / k
        return sorted({min(total - 1, int(i * step)) for i in range(k)})


@CompressionRegistry.register("gather")
class GatherCompress(Compressor):
    """分段聚集：每段保留首尾（保留段边界信息，适合长文档）。"""

    def select(self, total: int, ratio: float) -> List[int]:
        k = max(1, int(total * ratio))
        if k >= total:
            return list(range(total))
        seg = max(1, total // max(1, k // 2))
        kept = set()
        for s in range(0, total, seg):
            kept.add(s)
            kept.add(min(total - 1, s + seg - 1))
        while len(kept) < k:
            for i in range(total):
                if i not in kept:
                    kept.add(i)
                    break
                if len(kept) >= k:
                    break
        return sorted(list(kept)[:k])


def get_compressor(name: str) -> Compressor:
    try:
        return CompressionRegistry.get(name)()
    except KeyError:
        raise KVError(f"未知压缩策略 {name!r}，可用：{CompressionRegistry.keys()}")
