# 变更日志

## 1.0.0（2026-09-11）

- 首个版本发布
- KV Cache 智能管理（预算/量化/压缩/驱逐/滑动/混合）
- 稀疏注意力（DeepSelect 风格 TopK + 四种模式 + 三种索引）
- CED 非对称推理引擎（分块/流式/投机解码）
- JIT 编译缓存（DeepJIT 风格，CUDA/昇腾）
- 协议转换（deepseek-recipe 风格，OpenAI 兼容）
- REST serving（FastAPI）+ Python SDK + CLI
- 9 张内置模型卡 + 完整文档 + Docker/K8s/CI
