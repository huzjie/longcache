"""JIT 编译后端：CUDA / 昇腾 NPU。"""
from longcache.jit.backends.cuda import CUDABackend
from longcache.jit.backends.ascend import AscendBackend

__all__ = ["CUDABackend", "AscendBackend"]
