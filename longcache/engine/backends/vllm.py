"""vLLM 后端：对接 vLLM OpenAI 兼容端点。"""
from __future__ import annotations

from typing import Any, Dict, List

from longcache.engine.backends.base import Backend


class VLLMBackend(Backend):
    """vLLM 后端（需配置 VLLM_BASE_URL）。真实环境用 HTTP 调用，此处保留接口。"""

    name = "vllm"

    def __init__(self, base_url: str | None = None):
        import os
        self.base_url = base_url or os.getenv("VLLM_BASE_URL", "http://127.0.0.1:8001")

    def prefill(self, prompt: str, n_encoder_layers: int) -> Dict[str, Any]:
        return {"prompt": prompt, "encoder_layers": n_encoder_layers}

    def decode(self, state: Dict[str, Any], max_new_tokens: int,
               n_decoder_layers: int, streaming: bool = True) -> List[int]:
        # 真实实现：POST {base_url}/v1/completions，解析返回 token
        return []
