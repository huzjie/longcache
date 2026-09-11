"""稀疏注意力单测。"""
from longcache.config.schema import SparseConfig
from longcache.sparse.selector import SparseSelector
from longcache.sparse.topk import TopKSelector


def test_topk_select():
    sel = TopKSelector(3)
    pairs = [(0, 1.0), (1, 0.5), (2, 0.8), (3, 0.2), (4, 0.9)]
    ids = sel.select(pairs)
    assert ids == [0, 4, 2]


def test_sparse_selector_small():
    sel = SparseSelector(SparseConfig(strategy="topk", topk=10, local_window=8))
    keys = sel.select(seq_len=100, query_pos=50)
    assert 0 < len(keys) <= 10
