"""JIT 编译缓存运行时（DeepJIT 风格）。

对应 DeepSeek 开源的 DeepJIT——支持 CUDA 与昇腾 NPU 的 JIT 编译与缓存运行时，
把「算子源码 → 编译产物」的映射缓存起来，避免重复编译，加速冷启动与算子分发。
"""
from longcache.jit.kernel_cache import KernelCache
from longcache.jit.keygen import make_cache_key

__all__ = ["KernelCache", "make_cache_key"]
