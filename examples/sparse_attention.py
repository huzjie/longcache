"""示例：稀疏注意力选择。"""
from longcache.config.schema import SparseConfig
from longcache.sparse.selector import SparseSelector

sel = SparseSelector(SparseConfig(strategy="topk", topk=128, local_window=512))
keys = sel.select(seq_len=100000, query_pos=99999)
print(f"从 100000 个键中选中 {len(keys)} 个：{keys[:10]}...")
