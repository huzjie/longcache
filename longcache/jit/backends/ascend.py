"""昇腾 NPU JIT 后端：描述 CANN 算子编译接口（无 NPU 时为桩）。"""
from __future__ import annotations

from typing import Any, Dict


class AscendBackend:
    """昇腾 NPU 后端。真实实现走 CANN 的 aclnn / te 编译，此处保留接口描述。

    DeepJIT 同时支持 CUDA 与昇腾 NPU，本后端对应国产算力场景。
    """

    name = "ascend"
    target_archs = ("ascend310", "ascend910")

    def compile(self, kernel_name: str, source: str, arch: str = "ascend910") -> Dict[str, Any]:
        return {"backend": "ascend", "kernel": kernel_name, "arch": arch, "status": "compiled"}

    def supported(self, arch: str) -> bool:
        return arch in self.target_archs
