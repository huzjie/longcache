# 协议转换（deepseek-recipe 风格）

## 背景

deepseek-recipe 负责 API 协议转换与提示词编解码，让不同模型都能接入统一的
OpenAI 兼容前端。

## 组件

| 组件 | 说明 |
|---|---|
| `codec` | 提示词编解码：messages ↔ 原生字符串 |
| `openai` | OpenAI 兼容请求体构造 / 解析 |
| `sse` | SSE 流式输出 |

## 支持的协议

- `/v1/chat/completions`（OpenAI 兼容）
- `/v1/completions`（OpenAI 兼容）
- `/v1/models`
