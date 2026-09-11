"""配置数据模型（纯 dataclass，无第三方依赖）。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class KVConfig:
    """KV Cache 管理配置。"""
    budget_bytes: int = 1_073_741_824          # 默认 1GB，对应 1M 上下文目标
    block_size: int = 64                       # 每块 token 数
    quant: str = "fp4"                         # none|fp4|int8
    eviction: str = "lru"                      # lru|fifo|lfu
    sliding_window: int = 0                    # 0 表示不启用滑动窗口
    compression: str = "topk"                  # none|topk|avgpool|gather
    compression_ratio: float = 0.25            # 压缩后保留比例
    hybrid: bool = False                       # 是否启用 满窗口 + 滑动窗口 混合
    max_seq_len: int = 1_048_576               # 最大上下文 token 数


@dataclass
class SparseConfig:
    """稀疏注意力配置。"""
    strategy: str = "topk"                     # topk|local|sliding|global
    topk: int = 256                            # DeepSelect 风格 TopK 每查询保留数
    local_window: int = 1024                   # 局部窗口大小
    index: str = "streaming"                   # streaming|cross_layer|hierarchical


@dataclass
class EngineConfig:
    """推理引擎配置。"""
    backend: str = "mock"                      # mock|vllm|sglang|ollama
    chunk_size: int = 8192                     # 分块推理块大小
    streaming: bool = True                     # 是否流式解码
    speculative: bool = False                  # 是否投机解码
    speculative_depth: int = 4
    max_new_tokens: int = 2048
    temperature: float = 0.7
    seed: int = 42


@dataclass
class JITConfig:
    """JIT 编译缓存配置。"""
    enabled: bool = True
    backend: str = "cuda"                      # cuda|ascend
    cache_dir: str = ".longcache_jit"
    max_entries: int = 4096


@dataclass
class ServingConfig:
    """REST 服务配置。"""
    host: str = "0.0.0.0"
    port: int = 8000
    openai_compat: bool = True
    enable_metrics: bool = True
    max_concurrent: int = 64


@dataclass
class RuntimeConfig:
    """运行时顶层配置。"""
    model: str = "deepseek-v4.1-flash"
    kv: KVConfig = field(default_factory=KVConfig)
    sparse: SparseConfig = field(default_factory=SparseConfig)
    engine: EngineConfig = field(default_factory=EngineConfig)
    jit: JITConfig = field(default_factory=JITConfig)
    serving: ServingConfig = field(default_factory=ServingConfig)
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "RuntimeConfig":
        def build(section: str, cls_, default):
            raw = d.get(section, {})
            if raw is None:
                raw = {}
            if isinstance(raw, dict):
                # 只注入 schema 已知字段
                known = {f.name for f in cls_.__dataclass_fields__.values()}
                return cls_(**{k: v for k, v in raw.items() if k in known})
            return default
        return cls(
            model=d.get("model", "deepseek-v4.1-flash"),
            kv=build("kv", KVConfig, KVConfig()),
            sparse=build("sparse", SparseConfig, SparseConfig()),
            engine=build("engine", EngineConfig, EngineConfig()),
            jit=build("jit", JITConfig, JITConfig()),
            serving=build("serving", ServingConfig, ServingConfig()),
            extra={k: v for k, v in d.items()
                   if k not in ("model", "kv", "sparse", "engine", "jit", "serving")},
        )
