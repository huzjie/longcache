"""SDK 单测。"""
from longcache.sdk.client import LongCacheClient


def test_client_generate():
    client = LongCacheClient()
    result = client.generate("测试", max_new_tokens=8)
    assert result["output_tokens"] == 8
    stats = client.stats()
    assert "kv" in stats
