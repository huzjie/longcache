"""延迟评测：TTFT / TPOT 统计。"""
from __future__ import annotations

import statistics
import time


def measure_latency(generate_fn, runs: int = 50) -> dict:
    """多次生成，统计首 token 延迟（TTFT）与每 token 延迟（TPOT）。"""
    ttfts = []
    tpots = []
    for _ in range(runs):
        start = time.time()
        n = 0
        for _ in generate_fn():
            if n == 0:
                ttfts.append((time.time() - start) * 1000)
            else:
                tpots.append(time.time() - start)
            n += 1
        if n == 0:
            ttfts.append((time.time() - start) * 1000)
    return {
        "ttft_ms_mean": statistics.mean(ttfts) if ttfts else 0,
        "ttft_ms_p95": _p95(ttfts),
        "tpot_ms_mean": statistics.mean(tpots) if tpots else 0,
        "runs": runs,
    }


def _p95(vals):
    if not vals:
        return 0
    s = sorted(vals)
    return s[int(len(s) * 0.95)]
