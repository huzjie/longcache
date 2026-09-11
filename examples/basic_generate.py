"""示例：进程内生成一段文本。"""
from longcache.sdk.client import LongCacheClient

client = LongCacheClient()
result = client.generate("介绍一下 KV Cache 压缩", max_new_tokens=32)
print("输入 tokens:", result["input_tokens"])
print("输出 tokens:", result["output_tokens"])
print("KV 统计:", client.stats()["kv"])
