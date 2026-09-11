"""模型列表路由（OpenAI 兼容 /v1/models）。"""
from __future__ import annotations

from fastapi import APIRouter

from longcache.models.loader import list_models

router = APIRouter(tags=["models"])


@router.get("/models")
async def models():
    data = [{"id": name, "object": "model", "owned_by": "longcache"}
            for name in list_models()]
    return {"object": "list", "data": data}
