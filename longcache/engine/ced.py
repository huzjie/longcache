"""CED 非对称引擎：Causal-Encoder-Decoder 结构的推理编排。

核心思想（对应 V4.1-Flash 的 CED）：
- 编码器（20 层因果编码器）对整段提示做一次 prefill（激活 ~8B）；
- 解码器（20 层解码器）按 token 自回归生成（激活 ~16B）；
- prefill 与 decode 的激活量不对称，分别调度 KV 与计算。
"""
from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from longcache.config.schema import RuntimeConfig
from longcache.core.logging import get_logger
from longcache.core.utils import stable_hash, now_ms
from longcache.engine.backends import get_backend
from longcache.models.spec import ModelSpec

log = get_logger("longcache.engine")


class CEDEngine:
    """Causal-Encoder-Decoder 推理引擎。"""

    def __init__(self, cfg: RuntimeConfig, model: Optional[ModelSpec] = None):
        self.cfg = cfg
        self.model = model
        self.backend = get_backend(cfg.engine.backend)
        self.n_encoder_layers = 20
        self.n_decoder_layers = 20

    def prefill(self, prompt: str) -> Dict[str, Any]:
        """编码阶段：对提示做因果编码，产出 KV 与摘要状态。"""
        return self.backend.prefill(prompt, self.n_encoder_layers)

    def decode(self, state: Dict[str, Any], max_new_tokens: int,
               streaming: bool = True) -> List[int]:
        """解码阶段：自回归生成 token id 序列。"""
        return self.backend.decode(state, max_new_tokens, self.n_decoder_layers,
                                   streaming=streaming)

    def generate(self, prompt: str, max_new_tokens: Optional[int] = None) -> Dict[str, Any]:
        """端到端生成：prefill -> decode。"""
        if max_new_tokens is None:
            max_new_tokens = self.cfg.engine.max_new_tokens
        state = self.prefill(prompt)
        ids = self.decode(state, max_new_tokens, streaming=self.cfg.engine.streaming)
        return {
            "input_tokens": state.get("input_tokens", 0),
            "output_tokens": len(ids),
            "token_ids": ids,
            "state": state,
        }


def run_mock_inference(model: Optional[ModelSpec], cfg: RuntimeConfig,
                       kv, sel, prompt: str) -> Dict[str, Any]:
    """mock 后端端到端推理（供 doctor 冒烟，无 GPU 无网络）。

    把 KV 写入、稀疏注意力选择、CED prefill/decode 串起来跑一遍，
    返回输入/输出 token 数与耗时。
    """
    t0 = now_ms()
    input_tokens = max(1, len(prompt) // 2)
    # 1. 编码阶段写入 KV（分块）
    for i in range(0, input_tokens, cfg.kv.block_size):
        chunk = prompt[i:i + cfg.kv.block_size]
        kv.write(0, i, chunk)
    # 2. 稀疏注意力选择（对输入 token 建索引）
    sel.build_index(list(range(input_tokens)))
    # 3. CED 生成
    engine = CEDEngine(cfg, model)
    result = engine.generate(prompt, max_new_tokens=min(cfg.engine.max_new_tokens, 64))
    # 4. 长上下文压缩演示
    kept = kv.compress_context(input_tokens)
    elapsed = now_ms() - t0
    return {
        "input_tokens": input_tokens,
        "output_tokens": result["output_tokens"],
        "kept_positions": len(kept),
        "elapsed_ms": elapsed,
    }
