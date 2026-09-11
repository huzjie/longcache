"""评测报告汇总。"""
from __future__ import annotations

import time

from longcache.config.schema import RuntimeConfig
from longcache.core.logging import get_logger
from longcache.core.utils import human_bytes
from longcache.models.loader import load_model
from longcache.kv.manager import KVManager
from longcache.sparse.selector import SparseSelector

log = get_logger("longcache.benchmark")


def run_benchmark(cfg: RuntimeConfig, steps: int = 1000) -> None:
    """跑一遍 mock 性能评测并打印报告。"""
    model = load_model(cfg.model)
    kv = KVManager(cfg.kv, model)
    sel = SparseSelector(cfg.sparse)

    # 模拟 steps 步生成
    t0 = time.time()
    for i in range(steps):
        kv.write(0, i * cfg.kv.block_size, f"token-block-{i}")
        sel.select(max(1, i + cfg.sparse.topk), min(i, 100))
    elapsed = time.time() - t0
    tps = steps / elapsed if elapsed else 0

    print("=== longcache benchmark ===")
    print(f"模型：{model.name}（{model.arch}，{model.params}）")
    print(f"KV 预算：{human_bytes(cfg.kv.budget_bytes)} / 每 token {kv.per_token_bytes:.1f}B")
    print(f"模拟步数：{steps}，耗时 {elapsed:.2f}s，{tps:.0f} steps/s")
    print(f"KV 命中率：{kv.hit_rate()*100:.1f}% / 驱逐：{kv.stats.evictions}")
    print(f"当前驻留：{human_bytes(kv.current_bytes())}（{len(kv._blocks)} 块）")
    print(f"压缩比：{kv.effective_ratio():.2f}x")
    print("=== benchmark 完成 ===")
