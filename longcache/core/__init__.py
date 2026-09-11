"""核心基础模块：异常、注册表、日志、工具函数。"""
from longcache.core.errors import (
    LongCacheError,
    ConfigError,
    KVError,
    SparseError,
    EngineError,
    JITError,
    ProtocolError,
    ServingError,
    ModelLoadError,
)
from longcache.core.registry import Registry

__all__ = [
    "LongCacheError",
    "ConfigError",
    "KVError",
    "SparseError",
    "EngineError",
    "JITError",
    "ProtocolError",
    "ServingError",
    "ModelLoadError",
    "Registry",
]
