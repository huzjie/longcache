"""内存预算：把 KV Cache 预算换算成可承载的 token 数 / 块数。"""
from __future__ import annotations

from dataclasses import dataclass

from longcache.core.utils import human_bytes


@dataclass
class MemoryBudget:
    """KV Cache 内存预算。

    ``budget_bytes`` 是总预算；``bytes_per_token`` 是量化后每 token 的 KV 字节数。
    由此推导 ``max_tokens``（可同时驻留的 token 数）与 ``max_blocks``。
    """
    budget_bytes: int
    bytes_per_token: float
    block_size: int = 64

    @property
    def max_tokens(self) -> int:
        if self.bytes_per_token <= 0:
            return 0
        return int(self.budget_bytes / self.bytes_per_token)

    @property
    def max_blocks(self) -> int:
        return max(1, self.max_tokens // self.block_size)

    def describe(self) -> str:
        return (
            f"预算 {human_bytes(self.budget_bytes)} / 每 token {self.bytes_per_token:.1f}B "
            f"-> 可驻留 {self.max_tokens:,} tokens（{self.max_blocks:,} 块）"
        )


def simulate_budget(context_len: int, budget_bytes: int) -> None:
    """`longcache compress` 命令：模拟不同量化位宽下的缓存占用。

    DeepSeek V4.1-Flash 通过 CED 非对称结构把每 token 的 KV 元素数大幅压缩，
    配合 FP4 量化后每 token 仅 890 字节。这里以该标称值为 FP4 基准，反推
    FP8 / FP16 的占用，直观说明「只有 FP4 才能把 1M 上下文压进 1GB」。
    """
    fp4_per_token = 890.0  # V4.1-Flash 标称：每 token KV 890 字节（FP4）

    print("KV Cache 压缩预算模拟")
    print(f"上下文长度：{context_len:,} tokens | 预算：{human_bytes(budget_bytes)}")
    print("基准：DeepSeek V4.1-Flash CED 结构，FP4 每 token 890 字节")
    print("-" * 66)
    print(f"{'位宽':<16}{'每token字节':>12}{'1M上下文占用':>16}{'是否达标':>10}")
    print("-" * 66)

    ok = False
    for label, per_token in (
        ("FP16（无量化）", fp4_per_token * 4),
        ("BF16（无量化）", fp4_per_token * 4),
        ("FP8", fp4_per_token * 2),
        ("FP4", fp4_per_token),
    ):
        total = per_token * context_len
        within = total <= budget_bytes
        if within:
            ok = True
        print(f"{label:<16}{per_token:>11.0f}B{human_bytes(total):>16}{('OK 达标' if within else '超预算'):>10}")
    print("-" * 66)
    if ok:
        print(f"结论：FP4 量化即可把 {context_len:,} tokens 上下文压入 {human_bytes(budget_bytes)}")
    else:
        print("结论：当前预算无法容纳，请提高 budget_bytes 或降低量化位宽")


def estimate_bytes_per_token(width: float, heads_kv: int, layers: int, head_dim: int) -> float:
    """按结构估算每 token KV 字节数（K+V 两个矩阵）。"""
    return heads_kv * layers * head_dim * width
