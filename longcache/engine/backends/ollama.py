"""Ollama 后端：对接本地 Ollama 服务。"""
from __future__ import annotations

from typing import Any, Dict, List

from longcache.engine.backends.base import Backend


class OllamaBackend(Backend):
    """Ollama 后端（需配置 OLLAMA_BASE_URL）。"""

    name = "ollama"

    def __init__(self, base_url: str | None = None):
        import os
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")

    def prefill(self, prompt: str, n_encoder_layers: int) -> Dict[str, Any]:
        return {"prompt": prompt, "encoder_layers": n_encoder_layers}

    def decode(self, state: Dict[str, Any], max_new_tokens: int,
               n_decoder_layers: int, streaming: bool = True) -> List[int]:
        return []
