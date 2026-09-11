"""通用注册表：按名字登记可插拔组件（策略 / 后端 / 量化器 / 驱逐算法等）。"""
from __future__ import annotations

from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar

T = TypeVar("T")


class Registry(Generic[T]):
    """一个按字符串键登记构造器的注册表。

    使用方式：装饰器 ``@Registry.register("key")`` 登记一个类或工厂函数，
    再通过 ``Registry.get("key")`` 取回。
    """

    def __init__(self, name: str = "registry"):
        self.name = name
        self._entries: Dict[str, T] = {}

    def register(self, key: str) -> Callable[[T], T]:
        def decorator(obj: T) -> T:
            if key in self._entries:
                raise KeyError(f"{self.name}: duplicate key {key!r}")
            self._entries[key] = obj
            return obj
        return decorator

    def get(self, key: str) -> T:
        if key not in self._entries:
            raise KeyError(
                f"{self.name}: key {key!r} not found. available: "
                f"{sorted(self._entries)}"
            )
        return self._entries[key]

    def get_optional(self, key: str, default: Optional[T] = None) -> Optional[T]:
        return self._entries.get(key, default)

    def keys(self) -> List[str]:
        return sorted(self._entries)

    def __contains__(self, key: str) -> bool:
        return key in self._entries

    def __len__(self) -> int:
        return len(self._entries)
