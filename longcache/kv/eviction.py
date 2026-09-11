"""驱逐策略：LRU / FIFO / LFU（可插拔注册表）。"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from longcache.core.registry import Registry
from longcache.core.errors import KVError
from longcache.kv.block import KVBlock

EvictionPolicyRegistry = Registry("eviction")


class EvictionPolicy(ABC):
    """驱逐策略抽象：从块表中选择要驱逐的块。"""

    name: str = "base"

    @abstractmethod
    def select_victim(self, blocks: List[KVBlock]) -> Optional[KVBlock]:
        """从候选块里挑一个受害者。"""


@EvictionPolicyRegistry.register("lru")
class LRU(EvictionPolicy):
    name = "lru"

    def select_victim(self, blocks: List[KVBlock]) -> Optional[KVBlock]:
        if not blocks:
            return None
        return min(blocks, key=lambda b: b.last_access)


@EvictionPolicyRegistry.register("fifo")
class FIFO(EvictionPolicy):
    name = "fifo"

    def select_victim(self, blocks: List[KVBlock]) -> Optional[KVBlock]:
        if not blocks:
            return None
        return min(blocks, key=lambda b: b.block_id)


@EvictionPolicyRegistry.register("lfu")
class LFU(EvictionPolicy):
    name = "lfu"

    def select_victim(self, blocks: List[KVBlock]) -> Optional[KVBlock]:
        if not blocks:
            return None
        return min(blocks, key=lambda b: (b.access_count, b.last_access))


def get_eviction(name: str) -> EvictionPolicy:
    try:
        return EvictionPolicyRegistry.get(name)()
    except KeyError:
        raise KVError(f"未知驱逐策略 {name!r}，可用：{EvictionPolicyRegistry.keys()}")
