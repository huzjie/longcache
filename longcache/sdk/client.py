"""进程内 SDK 客户端：无需 HTTP，直接调用引擎。"""
from __future__ import annotations

from typing import List, Optional

from longcache.config.schema import RuntimeConfig
from longcache.config.loader import load_config
from longcache.engine.ced import CEDEngine
from longcache.kv.manager import KVManager
from longcache.models.loader import load_model
from longcache.sparse.selector import SparseSelector


class LongCacheClient:
    """进程内客户端，封装「模型 + KV + 稀疏 + 引擎」为一个门面。"""

    def __init__(self, config_path: Optional[str] = None, config: Optional[RuntimeConfig] = None):
        self.cfg = config or load_config(config_path)
        self.model = load_model(self.cfg.model)
        self.kv = KVManager(self.cfg.kv, self.model)
        self.sparse = SparseSelector(self.cfg.sparse)
        self.engine = CEDEngine(self.cfg, self.model)

    def generate(self, prompt: str, max_new_tokens: Optional[int] = None) -> dict:
        """生成文本（mock 后端返回 token id 序列 + 元数据）。"""
        result = self.engine.generate(prompt, max_new_tokens=max_new_tokens)
        # 写入 KV 并做稀疏选择（演示长上下文处理链路）
        self.kv.write(0, 0, prompt)
        self.sparse.build_index(list(range(result["input_tokens"])))
        return result

    def stats(self) -> dict:
        return {"kv": self.kv.describe(), "sparse": self.sparse.describe()}
