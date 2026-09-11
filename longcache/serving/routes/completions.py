"""Completions 路由（OpenAI 兼容）。"""
from __future__ import annotations

from fastapi import APIRouter, Request
from pydantic import BaseModel

from longcache.serving.metrics import METRICS

router = APIRouter(tags=["completions"])


class CompletionRequest(BaseModel):
    model: str = "deepseek-v4.1-flash"
    prompt: str
    max_tokens: int = 256
    temperature: float = 0.7
    stream: bool = False


@router.post("/completions")
async def completions(req: CompletionRequest, request: Request):
    METRICS.incr("completions_total")
    from longcache.engine.backends.mock import MockBackend
    backend = MockBackend()
    state = backend.prefill(req.prompt, 20)
    ids = backend.decode(state, min(req.max_tokens, 256), 20)
    text = " ".join(f"<t{i % 1000}>" for i in ids[:32])
    return {
        "id": "cmpl-longcache",
        "object": "text_completion",
        "model": req.model,
        "choices": [{"index": 0, "text": text, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": len(req.prompt) // 2, "completion_tokens": len(ids)},
    }
