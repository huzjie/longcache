"""混合缓存单测。"""
from longcache.kv.compression import get_compressor
from longcache.kv.hybrid import HybridCache


def test_hybrid_ratio():
    hc = HybridCache(window_size=1024, compress_ratio=0.1)
    hc.update(total=100000, compressor=get_compressor("topk"))
    ratio = hc.ratio(100000)
    assert 0.0 < ratio < 0.3
