"""滑动窗口：只保留最近 N 个 token 的 KV（配合满窗口做混合）。"""
from __future__ import annotations

from typing import List


class SlidingWindow:
    """滑动窗口状态：维护一个序列的窗口内 token 位置集合。"""

    def __init__(self, window_size: int):
        self.window_size = window_size
        self._positions: List[int] = []

    def push(self, pos: int) -> None:
        self._positions.append(pos)
        if self.window_size > 0 and len(self._positions) > self.window_size:
            self._positions = self._positions[-self.window_size:]

    @property
    def positions(self) -> List[int]:
        return list(self._positions)

    def __len__(self) -> int:
        return len(self._positions)
