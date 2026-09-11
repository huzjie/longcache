"""内存评测：KV Cache 占用 vs 上下文长度。"""
from __future__ import annotations

from longcache.core.utils import human_bytes


def memory_curve(per_token_bytes: float, context_lens: list) -> list:
    """计算不同上下文长度下的 KV 占用曲线。"""
    rows = []
    for ctx in context_lens:
        rows.append({
            "context_len": ctx,
            "kv_bytes": per_token_bytes * ctx,
            "kv_human": human_bytes(per_token_bytes * ctx),
        })
    return rows


def print_memory_table(per_token_bytes: float) -> None:
    print("KV Cache 内存曲线（每 token %.1f B）" % per_token_bytes)
    print("-" * 50)
    for row in memory_curve(per_token_bytes, [4096, 16384, 65536, 131072, 262144, 524288, 1048576]):
        print(f"{row['context_len']:>10,} tokens -> {row['kv_human']:>10}")
