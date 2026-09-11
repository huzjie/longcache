"""分块推理：把超长提示按 chunk_size 切块，逐块 prefill 并复用 KV。

这是 1M 上下文推理的关键——不可能一次性把 1M token 全塞进显存 prefill，
必须分块处理并配合 KV Cache 压缩/驱逐。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from longcache.core.utils import chunked, stable_hash


@dataclass
class ChunkState:
    """分块处理状态。"""
    chunk_size: int
    processed_tokens: int = 0
    chunk_boundaries: List[int] = field(default_factory=list)

    def feed(self, tokens: List[int]) -> List[List[int]]:
        """喂入 token 流，返回按块切好的子序列。"""
        out = []
        for ch in chunked(tokens, self.chunk_size):
            out.append(list(ch))
            self.processed_tokens += len(ch)
            self.chunk_boundaries.append(self.processed_tokens)
        return out

    def is_boundary(self, pos: int) -> bool:
        return pos in self.chunk_boundaries


def tokenize(text: str) -> List[int]:
    """确定性 mock 分词：每 2 字符一个 token（真实实现为 BPE）。"""
    if not text:
        return []
    return [stable_hash(text[i:i + 2], 24) for i in range(0, len(text), 2)]


def detokenize(ids: List[int]) -> str:
    """mock 反分词：把 token id 还原为占位文本。"""
    return " ".join(f"<t{id_ % 1000}>" for id_ in ids)
