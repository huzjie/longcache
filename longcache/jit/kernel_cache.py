"""Kernel 编译缓存：内存 LRU 缓存 + 可选磁盘持久化。"""
from __future__ import annotations

import json
import os
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, Optional

from longcache.core.errors import JITError
from longcache.core.logging import get_logger
from longcache.core.utils import now_ms
from longcache.jit.keygen import make_cache_key

log = get_logger("longcache.jit")


class KernelCache:
    """算子编译产物缓存（LRU）。

    真实场景里 ``value`` 是编译后的 kernel 句柄；这里用 dict 元数据 + 状态
    表示，无 GPU 也能完整跑通「命中 / 未命中 / 编译 / 持久化 / 淘汰」全流程。
    """

    def __init__(self, max_entries: int = 4096, cache_dir: Optional[str] = None):
        self.max_entries = max_entries
        self.cache_dir = cache_dir
        self._store: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()
        self.hits = 0
        self.misses = 0
        self.compiles = 0
        if cache_dir:
            Path(cache_dir).mkdir(parents=True, exist_ok=True)
            self._load_disk()

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        if key in self._store:
            self._store.move_to_end(key)
            self.hits += 1
            return self._store[key]
        self.misses += 1
        return None

    def put(self, key: str, value: Dict[str, Any]) -> None:
        self._store[key] = value
        self._store.move_to_end(key)
        while len(self._store) > self.max_entries:
            self._store.popitem(last=False)  # 淘汰最久未用
        self._persist()

    def compile_and_cache(self, kernel_name: str, signature: str, backend: str,
                          extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """查找缓存，未命中则「编译」并缓存。返回编译产物元数据。"""
        key = make_cache_key(kernel_name, signature, backend, extra)
        hit = self.get(key)
        if hit is not None:
            return {"cache": "hit", "key": key, "entry": hit}

        # 模拟编译
        self.compiles += 1
        entry = {
            "kernel": kernel_name,
            "signature": signature,
            "backend": backend,
            "compiled_at_ms": now_ms(),
            "status": "compiled",
        }
        self.put(key, entry)
        return {"cache": "miss", "key": key, "entry": entry}

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total else 0.0

    def stats(self) -> Dict[str, Any]:
        return {
            "entries": len(self._store),
            "hits": self.hits,
            "misses": self.misses,
            "compiles": self.compiles,
            "hit_rate": round(self.hit_rate, 4),
        }

    def _persist(self) -> None:
        if not self.cache_dir:
            return
        try:
            path = Path(self.cache_dir) / "kernel_cache.json"
            path.write_text(json.dumps({
                "max_entries": self.max_entries,
                "entries": {k: v for k, v in self._store.items()},
            }, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError as e:  # noqa: BLE001
            log.warning("持久化 JIT 缓存失败：%s", e)

    def _load_disk(self) -> None:
        try:
            path = Path(self.cache_dir) / "kernel_cache.json"
            if path.exists():
                data = json.loads(path.read_text(encoding="utf-8"))
                for k, v in data.get("entries", {}).items():
                    self._store[k] = v
        except (OSError, json.JSONDecodeError) as e:  # noqa: BLE001
            log.warning("读取 JIT 缓存失败：%s", e)
