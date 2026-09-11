"""SSE（Server-Sent Events）流式输出工具。"""
from __future__ import annotations

import json
from typing import Any, Dict


def sse_event(data: Dict[str, Any], event: str = "message") -> str:
    """构造一条 SSE 事件字符串。"""
    payload = json.dumps(data, ensure_ascii=False)
    return f"event: {event}\ndata: {payload}\n\n"


def sse_done() -> str:
    """SSE 结束标记。"""
    return "data: [DONE]\n\n"


def sse_chunk(token_text: str, index: int) -> str:
    """构造一条增量 chunk 事件。"""
    return sse_event({"choices": [{"delta": {"content": token_text}, "index": 0}]})
