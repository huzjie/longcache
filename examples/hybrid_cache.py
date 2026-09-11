"""示例：混合缓存（满窗口 + 滑动窗口）。"""
from longcache.kv.compression import get_compressor
from longcache.kv.hybrid import HybridCache

hc = HybridCache(window_size=1024, compress_ratio=0.1)
hc.update(total=100000, compressor=get_compressor("topk"))
print(f"混合缓存保留比例：{hc.ratio(100000):.3f}（保留 {len(hc.kept_positions())} 个 token）")
