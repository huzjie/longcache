# CED 非对称推理引擎

## Causal-Encoder-Decoder

DeepSeek V4.1-Flash 采用全新的 Causal-Encoder-Decoder 非对称结构：

- **20 层因果编码器**：对整段提示做一次 prefill，激活约 8B；
- **20 层解码器**：按 token 自回归生成，激活约 16B。

prefill 与 decode 激活量不对称，因此可分别调度 KV 与计算资源。

## 分块推理

1M 上下文不可能一次性 prefill，必须分块：

```python
from longcache.engine.chunk import ChunkState, tokenize
state = ChunkState(chunk_size=8192)
chunks = state.feed(tokenize(long_text))
```

## 投机解码

decode 阶段激活高于 prefill，用 draft 模型并行起草 + 主模型验证，
命中则跳过多次前向，降低延迟。
