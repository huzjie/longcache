"""示例：模拟不同位宽下的 KV 内存占用。"""
from longcache.kv.budget import simulate_budget

simulate_budget(context_len=1_048_576, budget_bytes=1_073_741_824)
