"""JIT 缓存单测。"""
from longcache.jit.kernel_cache import KernelCache
from longcache.jit.keygen import make_kernel_signature


def test_compile_hit():
    cache = KernelCache(max_entries=128)
    sig = make_kernel_signature("fp16", (1, 128))
    r1 = cache.compile_and_cache("add", sig, "cuda")
    r2 = cache.compile_and_cache("add", sig, "cuda")
    assert r1["cache"] == "miss"
    assert r2["cache"] == "hit"
