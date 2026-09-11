"""KV 管理器单测。"""
from longcache.config.schema import KVConfig
from longcache.kv.manager import KVManager


def test_write_and_hit_rate():
    kv = KVManager(KVConfig(budget_bytes=1024 * 1024, block_size=64, quant="fp4"))
    kv.write(0, 0, "hello world " * 100)
    assert kv.stats.writes == 1
    assert 0.0 <= kv.hit_rate() <= 1.0


def test_eviction():
    kv = KVManager(KVConfig(budget_bytes=256, block_size=64, quant="fp4", eviction="lru"))
    for i in range(100):
        kv.write(i, i * 64, f"seq-{i}")
    assert kv.stats.evictions > 0


def test_compress_context():
    kv = KVManager(KVConfig(compression="topk", compression_ratio=0.25))
    kept = kv.compress_context(1000)
    assert 0 < len(kept) <= 1000
