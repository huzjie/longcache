# JIT 编译缓存（DeepJIT 风格）

## 背景

DeepJIT 是支持 CUDA 与昇腾 NPU 的 JIT 编译与缓存运行时，把算子源码→编译产物
的映射缓存起来，避免重复编译，加速冷启动。

## 组件

| 组件 | 说明 |
|---|---|
| `keygen` | 稳定缓存 key：sha256(kernel | signature | backend | options) |
| `kernel_cache` | LRU 缓存 + 可选磁盘持久化 |
| `backends/cuda` | CUDA 算子编译接口 |
| `backends/ascend` | 昇腾 NPU 算子编译接口 |

## 缓存 key

```
key = sha256(kernel_name | signature | backend | sorted(extra))[:16]
```

保证同一算子 + 同一签名 + 同一后端命中同一缓存。
