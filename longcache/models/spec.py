"""模型规格数据模型。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ModelSpec:
    """一张模型卡的完整描述。"""
    name: str
    vendor: str
    arch: str
    params: str
    total_params_b: float
    active_params_b: float
    context_len: int
    kv_cache_bytes_per_token: float
    heads_kv: int
    heads_q: int
    layers: int
    hidden_size: int
    license: str
    license_url: str
    description: str
    capabilities: List[str] = field(default_factory=list)
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ModelSpec":
        return cls(
            name=d["name"], vendor=d["vendor"], arch=d["arch"], params=d["params"],
            total_params_b=float(d["total_params_b"]),
            active_params_b=float(d["active_params_b"]),
            context_len=int(d["context_len"]),
            kv_cache_bytes_per_token=float(d["kv_cache_bytes_per_token"]),
            heads_kv=int(d["heads_kv"]), heads_q=int(d["heads_q"]),
            layers=int(d["layers"]), hidden_size=int(d["hidden_size"]),
            license=d["license"], license_url=d.get("license_url", ""),
            description=d["description"],
            capabilities=list(d.get("capabilities", [])),
            extra={k: v for k, v in d.items() if k not in {
                "name", "vendor", "arch", "params", "total_params_b",
                "active_params_b", "context_len", "kv_cache_bytes_per_token",
                "heads_kv", "heads_q", "layers", "hidden_size", "license",
                "license_url", "description", "capabilities"}},
        )
