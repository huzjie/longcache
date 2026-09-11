"""混合缓存策略：满窗口（全量） + 滑动窗口（最近）双轨，兼顾长程与局部。"""
from __future__ import annotations

from typing import List


class HybridCache:
    """把 KV 分为「全量长程」与「滑动窗口近程」两部分。

    全量部分走压缩（保留重要 token），窗口部分全保留，实现长上下文下
    既不掉长程信息、又保住局部连贯性的折中。
    """

    def __init__(self, window_size: int, compress_ratio: float):
        self.window_size = window_size
        self.compress_ratio = compress_ratio
        self._full: List[int] = []
        self._window: List[int] = []

    def update(self, total: int, compressor) -> None:
        """按当前总 token 数重算两部分的位置集合。"""
        if total <= self.window_size:
            self._full = []
            self._window = list(range(total))
            return
        self._window = list(range(total - self.window_size, total))
        # 长程部分用压缩器选重要位置
        self._full = compressor.select(total - self.window_size, self.compress_ratio)

    def kept_positions(self) -> List[int]:
        return sorted(set(self._full) | set(self._window))

    def ratio(self, total: int) -> float:
        if total <= 0:
            return 1.0
        return len(self.kept_positions()) / total
