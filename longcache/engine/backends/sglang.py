"""SGLang 后端：对接 SGLang 服务。"""
from __future__ import annotations

from typing import Any, Dict, List

from longcache.engine.backends.base import Backend


class SGLangBackend(Backend):
    """SGLang 后端（需配置 SGLANG_BASE_URL）。"""

    name = "sglang"

    def __init__(self, base_url: str | None = None):
        import os
        self.base_url = base_url or os.getenv("SGLANG_BASE_URL", "http://127.0.0.1:30000")

    def prefill(self, prompt: str, n_encoder_layers: int) -> Dict[str, Any]:
        return {"prompt": prompt, "encoder_layers": n_encoder_layers}

    def decode(self, state: Dict[str, Any], max_new_tokens: int,
               n_decoder_layers: int, streaming: bool = True) -> List[int]:
        return []
