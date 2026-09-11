"""推理引擎：CED 非对称结构、分块推理、流式解码、投机解码、多后端适配。

对应 DeepSeek V4.1-Flash 的 Causal-Encoder-Decoder（CED）非对称架构：
20 层因果编码器接 20 层解码器，prefill 激活 8B、decode 激活 16B。
"""
from longcache.engine.ced import CEDEngine, run_mock_inference
from longcache.engine.backends import get_backend

__all__ = ["CEDEngine", "run_mock_inference", "get_backend"]
