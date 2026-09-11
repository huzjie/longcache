"""模型卡单测。"""
from longcache.models.loader import load_model, list_models


def test_list_models():
    names = list_models()
    assert "deepseek-v4.1-flash" in names


def test_load_model():
    m = load_model("deepseek-v4.1-flash")
    assert m.context_len == 1048576
    assert m.kv_cache_bytes_per_token < 1000
