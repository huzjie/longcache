"""缓存 key 生成：把算子描述哈希成稳定 key。"""
from __future__ import annotations

from typing import Any, Dict

from longcache.core.utils import sha256_hex


def make_cache_key(kernel_name: str, signature: str, backend: str,
                   extra: Dict[str, Any] | None = None) -> str:
    """生成算子编译缓存的 key。

    key = sha256(kernel_name | signature | backend | sorted(extra))。
    保证同一算子 + 同一签名 + 同一后端 + 同一编译选项命中同一缓存。
    """
    parts = [kernel_name, signature, backend]
    if extra:
        parts.append(repr(sorted(extra.items())))
    return sha256_hex("|".join(parts))[:16]


def make_kernel_signature(dtype: str, shapes: tuple, flags: Dict[str, Any] | None = None) -> str:
    """生成算子签名字符串。"""
    s = f"{dtype}:{shapes}"
    if flags:
        s += ":" + repr(sorted(flags.items()))
    return s
