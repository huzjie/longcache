# 配置参考

配置支持 JSON（零依赖）与 YAML（需 PyYAML）。默认配置见 `config.example.json`。

## 完整字段

```json
{
  "model": "deepseek-v4.1-flash",
  "kv": {
    "budget_bytes": 1073741824,
    "block_size": 64,
    "quant": "fp4",
    "eviction": "lru",
    "sliding_window": 0,
    "compression": "topk",
    "compression_ratio": 0.25,
    "hybrid": false,
    "max_seq_len": 1048576
  },
  "sparse": {
    "strategy": "topk",
    "topk": 256,
    "local_window": 1024,
    "index": "streaming"
  },
  "engine": {
    "backend": "mock",
    "chunk_size": 8192,
    "streaming": true,
    "speculative": false,
    "speculative_depth": 4,
    "max_new_tokens": 2048,
    "temperature": 0.7,
    "seed": 42
  },
  "jit": {
    "enabled": true,
    "backend": "cuda",
    "cache_dir": ".longcache_jit",
    "max_entries": 4096
  },
  "serving": {
    "host": "0.0.0.0",
    "port": 8000,
    "openai_compat": true,
    "enable_metrics": true,
    "max_concurrent": 64
  }
}
```

## 可插拔组件

| 维度 | 可选值 |
|---|---|
| KV 量化 | none / fp8 / int8 / fp4 / int4 |
| KV 压缩 | none / topk / avgpool / gather |
| KV 驱逐 | lru / fifo / lfu |
| 稀疏模式 | local / sliding / global / block |
| 稀疏索引 | streaming / cross_layer / hierarchical |
| 推理后端 | mock / vllm / sglang / ollama |
| JIT 后端 | cuda / ascend |
