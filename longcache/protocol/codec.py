"""提示词编解码：chat / completion 模板之间的双向转换。"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Message:
    """一条对话消息。"""
    role: str
    content: str


class PromptCodec:
    """提示词编解码器。

    - encode：把结构化 messages 编码成模型原生提示词字符串；
    - decode：把原生字符串解析回 messages。
    """

    def __init__(self, template: str = "deepseek"):
        self.template = template

    def encode(self, messages: List[Message]) -> str:
        """编码为 DeepSeek 风格提示词（含特殊标记）。"""
        parts = []
        for m in messages:
            role = m.role
            if role == "system":
                parts.append(f"<|system|>\n{m.content}")
            elif role == "user":
                parts.append(f"<|user|>\n{m.content}")
            elif role == "assistant":
                parts.append(f"<|assistant|>\n{m.content}")
            else:
                parts.append(f"<|{role}|>\n{m.content}")
        parts.append("<|assistant|>")
        return "\n\n".join(parts)

    def decode(self, raw: str) -> List[Message]:
        """从原生字符串解析回 messages（简化实现）。"""
        messages: List[Message] = []
        for block in raw.split("\n\n"):
            if "\n" not in block:
                continue
            role, content = block.split("\n", 1)
            role = role.replace("<|", "").replace("|>", "")
            if role in ("system", "user", "assistant"):
                messages.append(Message(role=role, content=content))
        return messages


def messages_to_dicts(messages: List[Message]) -> List[Dict[str, str]]:
    return [{"role": m.role, "content": m.content} for m in messages]


def dicts_to_messages(dicts: List[Dict[str, str]]) -> List[Message]:
    return [Message(role=d.get("role", "user"), content=d.get("content", "")) for d in dicts]
