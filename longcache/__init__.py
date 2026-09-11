"""longcache — 超长上下文 MoE 推理引擎与 KV Cache 智能管理平台。

围绕 DeepSeek V4.1-Flash（552B MoE、Causal-Encoder-Decoder 非对称结构）的核心创新
「极致 KV Cache 压缩」与配套基础设施（DeepSelect 稀疏注意力 TopK、DeepJIT JIT
编译缓存、deepseek-recipe 协议转换）构建的工程化推理平台：把「KV 预算管理 →
量化压缩 → 稀疏注意力选择 → CED 分块推理 → 流式解码 → 协议转换 → 多后端
serving」工程化为一个填配置即运行、可直接部署的生产级推理基础设施。

顶层入口，导出版本与常用符号。
"""
from longcache.version import __version__, __author__, __license__, __description__

__all__ = ["__version__", "__author__", "__license__", "__description__"]
