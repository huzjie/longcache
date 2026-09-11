"""KV 量化器：FP16/BF16/FP8/FP4 位宽换算（可插拔注册表）。"""
from __future__ import annotations

from dataclasses import dataclass

from longcache.core.registry import Registry

QuantizerRegistry = Registry("quantizer")


@dataclass
class Quantizer:
    """一个量化位宽定义。``bytes_per_value`` 是每数值的字节数。"""
    name: str
    bytes_per_value: float
    description: str


# 预登记常用位宽
@QuantizerRegistry.register("none")
def _none() -> Quantizer:
    return Quantizer("none", 2.0, "不量化（FP16/BF16，每值 2 字节）")


@QuantizerRegistry.register("fp4")
def _fp4() -> Quantizer:
    return Quantizer("fp4", 0.5, "FP4 量化（每值 0.5 字节，1M 上下文 < 1GB 的关键）")


@QuantizerRegistry.register("fp8")
def _fp8() -> Quantizer:
    return Quantizer("fp8", 1.0, "FP8 量化（每值 1 字节）")


@QuantizerRegistry.register("int8")
def _int8() -> Quantizer:
    return Quantizer("int8", 1.0, "INT8 量化（每值 1 字节）")


@QuantizerRegistry.register("int4")
def _int4() -> Quantizer:
    return Quantizer("int4", 0.5, "INT4 量化（每值 0.5 字节）")


def get_quantizer(name: str) -> Quantizer:
    return QuantizerRegistry.get(name)()
