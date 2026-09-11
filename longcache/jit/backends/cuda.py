"""CUDA JIT 后端：描述 CUDA 算子编译接口（无 GPU 时为桩）。"""
from __future__ import annotations

from typing import Any, Dict


class CUDABackend:
    """CUDA 后端。真实实现调用 nvrtc / triton 编译，此处保留接口描述。"""

    name = "cuda"
    target_archs = ("sm_80", "sm_90", "sm_100")

    def compile(self, kernel_name: str, source: str, arch: str = "sm_90") -> Dict[str, Any]:
        return {"backend": "cuda", "kernel": kernel_name, "arch": arch, "status": "compiled"}

    def supported(self, arch: str) -> bool:
        return arch in self.target_archs
