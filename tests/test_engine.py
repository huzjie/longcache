"""引擎单测。"""
from longcache.config.loader import load_config
from longcache.engine.ced import CEDEngine


def test_generate():
    cfg = load_config()
    engine = CEDEngine(cfg)
    result = engine.generate("你好", max_new_tokens=16)
    assert result["output_tokens"] == 16
    assert result["input_tokens"] >= 1
