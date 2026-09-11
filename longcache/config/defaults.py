"""默认配置。"""
from __future__ import annotations

from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    "model": "deepseek-v4.1-flash",
    "kv": {
        "budget_bytes": 1073741824,
        "block_size": 64,
        "quant": "fp4",
        "eviction": "lru",
        "sliding_window": 0,
        "compression": "topk",
        "compression_ratio": 0.25,
        "hybrid": False,
        "max_seq_len": 1048576,
    },
    "sparse": {
        "strategy": "topk",
        "topk": 256,
        "local_window": 1024,
        "index": "streaming",
    },
    "engine": {
        "backend": "mock",
        "chunk_size": 8192,
        "streaming": True,
        "speculative": False,
        "speculative_depth": 4,
        "max_new_tokens": 2048,
        "temperature": 0.7,
        "seed": 42,
    },
    "jit": {
        "enabled": True,
        "backend": "cuda",
        "cache_dir": ".longcache_jit",
        "max_entries": 4096,
    },
    "serving": {
        "host": "0.0.0.0",
        "port": 8000,
        "openai_compat": True,
        "enable_metrics": True,
        "max_concurrent": 64,
    },
}
