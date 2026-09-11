"""稀疏注意力子系统：DeepSelect 风格 TopK 选择、稀疏模式、索引结构。

对应 DeepSeek 开源的 DeepSelect——加速稀疏注意力与采样中的 TopK 算子
（官方称比 torch.topk 快 2~20 倍）。本子系统提供纯 Python 的稀疏注意力
选择逻辑，可插拔到推理引擎中降低长上下文注意力复杂度。
"""
from longcache.sparse.topk import TopKSelector
from longcache.sparse.selector import SparseSelector
from longcache.sparse.pattern import SparsePatternRegistry

__all__ = ["TopKSelector", "SparseSelector", "SparsePatternRegistry"]
