"""吞吐评测：tokens/s 计算。"""
from __future__ import annotations

import time


def measure_throughput(generate_fn, total_tokens: int) -> dict:
    """测量生成 ``total_tokens`` 个 token 的吞吐。"""
    start = time.time()
    generated = generate_fn(total_tokens)
    elapsed = time.time() - start
    tps = generated / elapsed if elapsed > 0 else 0.0
    return {"tokens": generated, "elapsed_s": elapsed, "tokens_per_sec": tps}
