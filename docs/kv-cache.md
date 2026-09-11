# KV Cache 智能管理

## 问题

自回归生成中，每生成一个 token 都要重新计算所有历史 token 的 K/V 矩阵。
上下文越长，KV Cache 内存越大。DeepSeek V4.1-Flash 通过 FP4 量化 + 结构优化，
把每 token KV 占用压缩到 890 字节——是初代 V1 的 1/437，1M 上下文缓存不到 1GB。

## 组件

| 组件 | 说明 |
|---|---|
| `budget` | 内存预算：预算 / 每 token 字节 = 可驻留 token 数 |
| `block` | 块管理：按 `block_size` 切块，惰性分配 |
| `quant` | 量化：none / fp8 / int8 / fp4 / int4 |
| `compression` | 压缩：topk / avgpool / gather |
| `eviction` | 驱逐：lru / fifo / lfu |
| `sliding` | 滑动窗口：只保留最近 N token |
| `hybrid` | 混合：满窗口（压缩）+ 滑动窗口（全保留）|

## 内存估算公式

```
每 token KV 字节 = heads_kv × layers × head_dim × 位宽字节数 × 2 (K+V)
```

示例（近似 V4.1-Flash）：64 × 40 × 128 × 0.5 × 2 ≈ 327KB？——实际 DeepSeek
通过 CED 结构把 KV 头进一步压缩，标称 890B/token，以此为准。

## 用法

```bash
longcache compress --context-len 1048576 --budget-gb 1
```
