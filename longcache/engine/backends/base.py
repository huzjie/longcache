"""后端抽象基类。"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Backend(ABC):
    """推理后端抽象。"""

    name: str = "base"

    @abstractmethod
    def prefill(self, prompt: str, n_encoder_layers: int) -> Dict[str, Any]:
        """编码阶段，返回 KV 状态。"""

    @abstractmethod
    def decode(self, state: Dict[str, Any], max_new_tokens: int,
               n_decoder_layers: int, streaming: bool = True) -> List[int]:
        """解码阶段，返回 token id 列表。"""
