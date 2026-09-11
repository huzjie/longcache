"""协议转换子系统（deepseek-recipe 风格）。

对应 DeepSeek 开源的 deepseek-recipe——API 协议转换与提示词编解码，
用于把 OpenAI 兼容请求转换为 DeepSeek 原生协议、编码/解码提示词模板，
让不同模型都能接入统一的 OpenAI 兼容前端。
"""
from longcache.protocol.codec import PromptCodec
from longcache.protocol.openai import to_openai_chat, to_openai_completion
from longcache.protocol.sse import sse_event

__all__ = ["PromptCodec", "to_openai_chat", "to_openai_completion", "sse_event"]
