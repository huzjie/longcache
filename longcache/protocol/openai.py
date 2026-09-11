"""OpenAI 兼容协议转换。"""
from __future__ import annotations

from typing import Any, Dict, List

from longcache.protocol.codec import Message, dicts_to_messages


def to_openai_chat(messages: List[Dict[str, str]], model: str,
                   max_tokens: int = 2048, temperature: float = 0.7,
                   stream: bool = False) -> Dict[str, Any]:
    """构造 OpenAI 兼容的 chat.completions 请求体。"""
    return {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": stream,
    }


def to_openai_completion(prompt: str, model: str,
                         max_tokens: int = 2048, temperature: float = 0.7,
                         stream: bool = False) -> Dict[str, Any]:
    """构造 OpenAI 兼容的 completions 请求体。"""
    return {
        "model": model,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": stream,
    }


def from_openai_chat(request: Dict[str, Any]) -> List[Message]:
    """把 OpenAI chat 请求体解析为内部 Message 列表。"""
    raw = request.get("messages", [])
    return dicts_to_messages(raw)
