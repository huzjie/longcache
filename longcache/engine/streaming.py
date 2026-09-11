"""流式解码：按 token 产出增量结果（SSE 友好）。"""
from __future__ import annotations

import time
from typing import Generator, List


def stream_decode(generator: Generator[int, None, None], delay: float = 0.0):
    """把 token id 生成器包装为 (token_id, elapsed_ms) 流。"""
    t0 = time.time()
    for tid in generator:
        yield tid, (time.time() - t0) * 1000
        if delay:
            time.sleep(delay)


class StreamBuffer:
    """流式输出缓冲，支持增量拼接与片段回调。"""

    def __init__(self, on_delta=None):
        self.on_delta = on_delta
        self._acc: List[int] = []

    def add(self, token_id: int) -> None:
        self._acc.append(token_id)
        if self.on_delta:
            self.on_delta(token_id)

    @property
    def tokens(self) -> List[int]:
        return list(self._acc)
