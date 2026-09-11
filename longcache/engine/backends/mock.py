"""Mock 后端：确定性哈希驱动的离线实现，用于无 GPU 冒烟与单测。"""
from __future__ import annotations

from typing import Any, Dict, List

from longcache.core.utils import stable_hash
from longcache.engine.backends.base import Backend


class MockBackend(Backend):
    """mock 后端：不依赖任何真实模型，用确定性哈希生成 token。"""

    name = "mock"

    def prefill(self, prompt: str, n_encoder_layers: int) -> Dict[str, Any]:
        input_tokens = max(1, len(prompt) // 2)
        seed = stable_hash(prompt, 32)
        return {
            "input_tokens": input_tokens,
            "seed": seed,
            "encoder_layers": n_encoder_layers,
        }

    def decode(self, state: Dict[str, Any], max_new_tokens: int,
               n_decoder_layers: int, streaming: bool = True) -> List[int]:
        seed = state["seed"]
        ids: List[int] = []
        cur = seed
        for _ in range(max_new_tokens):
            cur = (cur * 1103515245 + 12345) & 0x7FFFFFFF
            ids.append(cur % 100000)
        return ids
