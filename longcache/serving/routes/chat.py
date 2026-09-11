"""Chat Completions 路由（OpenAI 兼容）。"""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Request
from pydantic import BaseModel

from longcache.protocol.codec import dicts_to_messages, PromptCodec
from longcache.serving.metrics import METRICS

router = APIRouter(tags=["chat"])


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str = "deepseek-v4.1-flash"
    messages: list[ChatMessage]
    max_tokens: int = 2048
    temperature: float = 0.7
    stream: bool = False


@router.post("/chat/completions")
async def chat_completions(req: ChatRequest, request: Request):
    cfg = request.app.state.cfg
    METRICS.incr("chat_completions_total")
    codec = PromptCodec()
    messages = dicts_to_messages([m.dict() for m in req.messages])
    encoded = codec.encode(messages)

    # 用 mock 后端生成（真实环境替换为 engine.generate）
    from longcache.engine.backends.mock import MockBackend
    backend = MockBackend()
    state = backend.prefill(encoded, 20)
    ids = backend.decode(state, min(req.max_tokens, 256), 20)

    reply = " ".join(f"<t{i % 1000}>" for i in ids[:32])
    return {
        "id": "chatcmpl-longcache",
        "object": "chat.completion",
        "model": req.model,
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": reply},
            "finish_reason": "stop",
        }],
        "usage": {"prompt_tokens": len(encoded) // 2, "completion_tokens": len(ids)},
    }
