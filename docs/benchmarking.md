# 性能评测

```bash
longcache bench --steps 1000
```

输出 KV 命中率、驱逐次数、驻留内存、压缩比等指标。

## 指标说明

| 指标 | 含义 |
|---|---|
| tokens/s | 生成吞吐 |
| TTFT | 首 token 延迟 |
| TPOT | 每 token 延迟 |
| KV 命中率 | 缓存复用比例 |
| 压缩比 | 量化后 vs FP16 的字节比 |
