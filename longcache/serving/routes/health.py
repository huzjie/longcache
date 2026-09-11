"""健康检查路由。"""
from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    return {"status": "ok", "service": "longcache"}


@router.get("/healthz")
async def healthz():
    return {"status": "ok"}
