# 稀疏注意力（DeepSelect 风格）

## 背景

全量注意力复杂度 O(n²)，1M 上下文下不可行。DeepSelect 加速稀疏注意力与采样
中的 TopK 算子（比 `torch.topk` 快 2~20 倍），只让每个查询关注最重要的 k 个键。

## 组件

| 组件 | 说明 |
|---|---|
| `topk` | 堆式 TopK 选择，O(n log k) |
| `pattern` | local / sliding / global / block 四种模式 |
| `index` | streaming（流感知）/ cross_layer（跨层）/ hierarchical（层级化）|

## 算法

```
对每个查询 q：
  1. 按模式取候选键集（如局部窗口）
  2. 若候选 > topk，用 TopK 选最重要的 k 个
  3. 仅对这 k 个键计算注意力
```

## 用法

```python
from longcache.sparse.selector import SparseSelector
from longcache.config.schema import SparseConfig

sel = SparseSelector(SparseConfig(strategy="topk", topk=256))
keys = sel.select(seq_len=1_000_000, query_pos=999_999)
```
