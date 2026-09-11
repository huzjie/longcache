"""量化器单测。"""
from longcache.kv.quant import get_quantizer


def test_fp4_smaller_than_fp16():
    fp16 = get_quantizer("none").bytes_per_value
    fp4 = get_quantizer("fp4").bytes_per_value
    assert fp4 < fp16
    assert fp4 == 0.5
