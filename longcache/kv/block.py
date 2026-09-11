"""KV 块：物理内存的最小管理单元。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class KVBlock:
    """一个 KV 块，容纳 ``block_size`` 个 token 的键值状态。

    ``data`` 是惰性占位的字节估算对象（真实实现中为张量），这里用字节数 +
    哈希指纹表示，保证无 GPU 依赖也能跑通全链路。
    """
    block_id: int
    seq_id: int
    start_pos: int
    block_size: int
    fingerprint: int = 0
    nbytes: int = 0
    last_access: float = 0.0
    access_count: int = 0
    data: Optional[Any] = field(default=None, repr=False)

    def touch(self, ts: float) -> None:
        self.last_access = ts
        self.access_count += 1


@dataclass
class BlockTable:
    """块表：seq -> 块链，管理一个序列的所有块。"""
    seq_id: int
    block_ids: list = field(default_factory=list)

    def append(self, bid: int) -> None:
        self.block_ids.append(bid)

    def __len__(self) -> int:
        return len(self.block_ids)
