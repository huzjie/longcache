"""统一异常体系。所有业务异常继承自 LongCacheError。"""


class LongCacheError(Exception):
    """longcache 根异常。"""


class ConfigError(LongCacheError):
    """配置加载或校验失败。"""


class ModelLoadError(LongCacheError):
    """模型卡加载失败。"""


class KVError(LongCacheError):
    """KV Cache 相关错误。"""


class SparseError(LongCacheError):
    """稀疏注意力相关错误。"""


class EngineError(LongCacheError):
    """推理引擎相关错误。"""


class JITError(LongCacheError):
    """JIT 编译缓存相关错误。"""


class ProtocolError(LongCacheError):
    """协议转换相关错误。"""


class ServingError(LongCacheError):
    """REST 服务相关错误。"""
