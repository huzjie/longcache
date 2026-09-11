"""投机解码：用小模型起草 + 大模型验证，降低解码延迟。

对应长上下文 decode 场景（decode 激活 16B 高于 prefill 8B），投机解码
用 draft 模型并行出 k 个候选，再由主模型一次验证，命中则跳过多次前向。
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SpeculativeConfig:
    depth: int = 4
    draft_accept_threshold: float = 0.5


class SpeculativeDecoder:
    """投机解码器（mock 实现：用确定性哈希模拟 draft 命中）。"""

    def __init__(self, depth: int = 4):
        self.depth = depth

    def draft(self, last_token: int) -> List[int]:
        """draft 模型并行起草 depth 个候选。"""
        out = []
        t = last_token
        for _ in range(self.depth):
            t = (t * 1103515245 + 12345) & 0x7FFFFFFF
            out.append(t % 1000)
        return out

    def verify(self, drafted: List[int], last_token: int) -> List[int]:
        """主模型验证：返回可接受的候选前缀。"""
        accepted: List[int] = []
        t = last_token
        for d in drafted:
            t = (t * 1103515245 + 12345) & 0x7FFFFFFF
            # 确定性「命中」判定
            if (t >> 16) & 1:
                accepted.append(d)
            else:
                break
        return accepted
