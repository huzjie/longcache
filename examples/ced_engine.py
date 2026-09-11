"""示例：CED 非对称引擎分阶段推理。"""
from longcache.config.loader import load_config
from longcache.engine.ced import CEDEngine

cfg = load_config()
engine = CEDEngine(cfg)
state = engine.prefill("你好，介绍一下 Causal-Encoder-Decoder 架构")
ids = engine.decode(state, max_new_tokens=16, streaming=True)
print("生成 token 数:", len(ids))
print("编码层数:", state["encoder_layers"])
