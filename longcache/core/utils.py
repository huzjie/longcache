"""通用工具函数。"""
from __future__ import annotations

import hashlib
import json
import time
from typing import Any, Iterable, List, Sequence


def human_bytes(n: float) -> str:
    """把字节数格式化为可读字符串。"""
    n = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB", "PB"):
        if abs(n) < 1024.0 or unit == "PB":
            return f"{n:.2f}{unit}" if unit != "B" else f"{int(n)}B"
        n /= 1024.0
    return f"{n:.2f}PB"


def human_number(n: float) -> str:
    """把大数字格式化为 K/M/B。"""
    n = float(n)
    for unit in ("", "K", "M", "B", "T"):
        if abs(n) < 1000.0 or unit == "T":
            return f"{n:.1f}{unit}" if unit else f"{int(n)}"
        n /= 1000.0
    return f"{n:.1f}T"


def now_ms() -> int:
    """当前毫秒时间戳。"""
    return int(time.time() * 1000)


def stable_hash(text: str, bits: int = 64) -> int:
    """对文本做确定性哈希（FNV-1a 变体），用于 mock 嵌入与缓存 key。"""
    h = 14695981039346656037
    data = text.encode("utf-8")
    for b in data:
        h ^= b
        h = (h * 1099511628211) & ((1 << 64) - 1)
    if bits < 64:
        h = h % (1 << bits)
    return h


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def chunked(seq: Sequence, size: int) -> Iterable[Sequence]:
    """把序列按 size 切块。"""
    for i in range(0, len(seq), size):
        yield seq[i:i + size]


def json_dump(obj: Any, indent: int = 2) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=indent, default=str)


def cosine_sim(a: List[float], b: List[float]) -> float:
    """两向量的余弦相似度。"""
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)
