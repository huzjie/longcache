"""KV Cache 管理子系统：预算、块、量化、压缩、驱逐、滑动窗口、管理器、混合策略。

这是 longcache 的核心——围绕 DeepSeek V4.1-Flash「每 token 890 字节、1M 上下文
缓存 < 1GB」的极致压缩目标，把 KV Cache 的生命周期（分配 → 写入 → 量化 →
压缩 → 驱逐 → 命中统计）工程化为可配置、可插拔的组件。
"""
from longcache.kv.manager import KVManager
from longcache.kv.budget import MemoryBudget, simulate_budget
from longcache.kv.quant import QuantizerRegistry, Quantizer
from longcache.kv.eviction import EvictionPolicyRegistry

__all__ = [
    "KVManager",
    "MemoryBudget",
    "simulate_budget",
    "QuantizerRegistry",
    "Quantizer",
    "EvictionPolicyRegistry",
]
