"""端到端自检：不依赖 GPU / 外部服务，mock 后端跑通全链路。"""
from __future__ import annotations

from longcache.config.schema import RuntimeConfig
from longcache.core.logging import get_logger
from longcache.core.utils import human_bytes
from longcache.models.loader import load_model

log = get_logger("longcache.doctor")


def run_doctor(cfg: RuntimeConfig) -> bool:
    """跑一遍全链路并打印报告。成功返回 True。"""
    log.info("=== longcache doctor 自检 ===")

    # 1. 模型卡
    model = load_model(cfg.model)
    log.info("[1/5] 模型卡加载 OK：%s（%s，%s）",
             model.name, model.arch, model.params)

    # 2. KV 预算
    from longcache.kv.manager import KVManager
    kv = KVManager(cfg.kv, model)
    log.info("[2/5] KV 管理器 OK：预算 %s / 块 %d / 量化 %s",
             human_bytes(cfg.kv.budget_bytes), cfg.kv.block_size, cfg.kv.quant)

    # 3. 稀疏注意力
    from longcache.sparse.selector import SparseSelector
    sel = SparseSelector(cfg.sparse)
    log.info("[3/5] 稀疏注意力 OK：策略 %s / topk %d",
             cfg.sparse.strategy, cfg.sparse.topk)

    # 4. CED 推理（mock）
    from longcache.engine.ced import run_mock_inference
    result = run_mock_inference(model, cfg, kv, sel, prompt="你好，介绍一下 DeepSeek V4.1-Flash 的 KV Cache 压缩技术。")
    log.info("[4/5] CED 推理 OK：%d tokens 输入 -> %d tokens 输出，耗时 %.1fms",
             result["input_tokens"], result["output_tokens"], result["elapsed_ms"])

    # 5. 汇总
    log.info("[5/5] 汇总：KV 命中率 %.1f%% / 压缩比 %.2fx / 峰值内存 %s",
             kv.hit_rate() * 100, kv.effective_ratio(), human_bytes(kv.current_bytes()))
    log.info("=== doctor 通过 ===")
    return True
