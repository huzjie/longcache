"""配置加载单测。"""
from longcache.config.loader import load_config
from longcache.config.schema import RuntimeConfig


def test_default_config():
    cfg = load_config()
    assert isinstance(cfg, RuntimeConfig)
    assert cfg.model == "deepseek-v4.1-flash"
    assert cfg.kv.quant == "fp4"
