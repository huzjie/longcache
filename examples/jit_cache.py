"""示例：JIT 编译缓存命中/未命中。"""
from longcache.jit.kernel_cache import KernelCache
from longcache.jit.keygen import make_kernel_signature

cache = KernelCache(max_entries=1024)
sig = make_kernel_signature("fp16", (1, 8192, 128))

r1 = cache.compile_and_cache("topk_forward", sig, "cuda")
r2 = cache.compile_and_cache("topk_forward", sig, "cuda")
print("第一次:", r1["cache"], "| 第二次:", r2["cache"])
print("缓存统计:", cache.stats())
