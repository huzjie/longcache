# longcache

<p align="center">
  <b>超长上下文 MoE 推理引擎与 KV Cache 智能管理平台</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue" alt="python">
  <img src="https://img.shields.io/badge/License-Apache%202.0-green" alt="license">
  <img src="https://img.shields.io/badge/Context-1M-orange" alt="context">
  <img src="https://img.shields.io/badge/Model-DeepSeek%20V4.1%20Flash-purple" alt="model">
  <img src="https://img.shields.io/badge/KV%20Cache-890B%2Ftoken-red" alt="kv">
</p>

> 灵感来源：**DeepSeek V4.1-Flash**（2026-09-11 开源）—— 552B MoE、全新
> Causal-Encoder-Decoder 非对称结构、KV Cache 每 token 仅 890 字节（初代 1/437）、
> 1M 上下文缓存不到 1GB、MIT 许可。配套开源 deepseek-recipe / DeepSelect /
> DeepJIT 三个基础设施仓库。

## 这是什么

`longcache` 不是「复刻一个模型」，而是把 V4.1-Flash 背后的**工程方法论**做成一个
**填配置即运行、可直接部署**的生产级推理基础设施：

| 热点技术 | longcache 落地为 |
|---|---|
| CED 非对称结构 | 编码器/decode 分离的推理引擎（分块 + 流式 + 投机解码）|
| 极致 KV Cache 压缩 | KV 预算 → 量化（FP4）→ 压缩（TopK）→ 驱逐（LRU）全链路 |
| DeepSelect 稀疏 TopK | 堆式 TopK 选择器 + 四种稀疏模式 + 三种索引结构 |
| DeepJIT JIT 编译缓存 | kernel 编译缓存（LRU + 磁盘持久化，CUDA/昇腾）|
| deepseek-recipe 协议转换 | OpenAI 兼容协议 + 提示词编解码 + SSE |

**核心卖点**：无 GPU、无外部服务也能端到端跑通全链路（mock 后端 + 哈希指纹），
填好配置、`pip install -e .` 后 `longcache doctor` 立即自检通过。

## 快速开始

```bash
git clone https://github.com/huzjie/longcache.git
cd longcache
pip install -e .

longcache doctor                                    # 自检（模型卡 + KV + 稀疏 + CED 推理）
longcache list-models                               # 列出 9 张内置模型卡
longcache compress --context-len 1048576 --budget-gb 1   # KV 压缩预算模拟
longcache bench --steps 1000                        # 性能评测
longcache serve --port 8000                         # REST 服务（/docs 交互文档）
```

Python SDK：

```python
from longcache.sdk.client import LongCacheClient

client = LongCacheClient()
result = client.generate("介绍一下 KV Cache 压缩", max_new_tokens=32)
print(client.stats())
```

## 核心能力

- 🧠 **KV Cache 智能管理**：内存预算换算 → 块管理 → FP4/INT8 量化 → TopK/池化/采样压缩 →
  LRU/FIFO/LFU 驱逐 → 滑动窗口 → 满窗口+滑动窗口混合，一条链把 1M 上下文压进 1GB
- 🎯 **稀疏注意力**（DeepSelect 风格）：堆式 TopK（O(n log k)）、local/sliding/global/block
  四模式、streaming/cross_layer/hierarchical 三索引
- ⚙️ **CED 非对称引擎**：20 层因果编码器 + 20 层解码器，分块 prefill + 流式 decode + 投机解码
- ⚡ **JIT 编译缓存**（DeepJIT 风格）：kernel 缓存 key 生成 + LRU + 磁盘持久化，CUDA/昇腾后端
- 🔌 **协议转换**（deepseek-recipe 风格）：OpenAI 兼容 `/v1/chat/completions`、`/v1/completions`、
  `/v1/models` + 提示词编解码 + SSE
- 🌐 **三入口**：CLI / FastAPI REST（OpenAI 兼容）/ Python SDK
- 📦 **9 张内置模型卡**：V4.1-Flash、V4-Flash、V3.2、R1、Kimi K3、Qwen3.5-4B、MiniCPM5-2B、
  LongCat-2.0、Smaug-Agentic（JSON，零依赖加载）
- 🧪 **离线可跑**：mock 后端 + 哈希指纹，无 GPU 无网络端到端跑通
- 🚀 **完整交付**：Docker 多阶段 + Compose + K8s（Deployment/Service/HPA/ConfigMap）+ CI

## 架构

```
CLI / SDK / REST(OpenAI)  →  serving + protocol  →  engine(CED/分块/流式/投机)
                                        ↓
                              sparse(TopK/模式/索引)
                                        ↓
                              kv(预算/量化/压缩/驱逐)
                                        ↓
                              jit(kernel 缓存) + config/core/models
```

详见 [`docs/architecture.md`](docs/architecture.md)。

## 配置

零依赖 JSON（或 YAML，需 PyYAML）。见 [`config.example.json`](config.example.json) 与
[`docs/config-reference.md`](docs/config-reference.md)。

可插拔组件一览：

| 维度 | 可选值 |
|---|---|
| KV 量化 | none / fp8 / int8 / fp4 / int4 |
| KV 压缩 | none / topk / avgpool / gather |
| KV 驱逐 | lru / fifo / lfu |
| 稀疏模式 | local / sliding / global / block |
| 推理后端 | mock / vllm / sglang / ollama |
| JIT 后端 | cuda / ascend |

## 文档

| 文档 | 说明 |
|---|---|
| [architecture](docs/architecture.md) | 架构设计 |
| [kv-cache](docs/kv-cache.md) | KV Cache 管理 |
| [sparse-attention](docs/sparse-attention.md) | 稀疏注意力 |
| [ced-engine](docs/ced-engine.md) | CED 推理引擎 |
| [jit](docs/jit.md) | JIT 编译缓存 |
| [protocol](docs/protocol.md) | 协议转换 |
| [serving](docs/serving.md) | REST 服务 |
| [config-reference](docs/config-reference.md) | 配置参考 |
| [benchmarking](docs/benchmarking.md) | 性能评测 |
| [deployment](docs/deployment.md) | 部署 |
| [contributing](docs/contributing.md) | 贡献指南 |
| [changelog](docs/changelog.md) | 变更日志 |
| [roadmap](docs/roadmap.md) | 路线图 |

## 目录结构

```
longcache/
├── longcache/            # 主包
│   ├── core/             # 异常/注册表/日志/工具
│   ├── config/           # 配置 schema/loader/defaults
│   ├── models/           # 模型卡（JSON）+ 加载器
│   ├── kv/               # KV Cache 管理（核心）
│   ├── sparse/           # 稀疏注意力（DeepSelect）
│   ├── engine/           # CED 推理引擎 + 多后端
│   ├── jit/              # JIT 编译缓存（DeepJIT）
│   ├── protocol/         # 协议转换（deepseek-recipe）
│   ├── serving/          # FastAPI REST
│   ├── benchmark/        # 性能评测
│   ├── sdk/              # Python SDK
│   ├── doctor.py         # 端到端自检
│   └── cli.py            # 命令行入口
├── examples/             # 示例脚本
├── tests/                # 单元测试
├── docs/                 # 文档
├── deploy/               # K8s / systemd
├── .github/              # CI / Release / Dependabot
├── Dockerfile / docker-compose.yml / Makefile
└── pyproject.toml / setup.py / requirements.txt
```

## 质量

- 零语法错误（`python -m compileall` 通过）
- 端到端自检 `longcache doctor` 通过（mock 后端）
- 单元测试覆盖 KV / 稀疏 / 量化 / 配置 / 模型 / JIT / 协议 / 引擎 / SDK / 混合
- Docker 多阶段 + Compose + K8s + 多 Python 版本 CI

## License

Apache 2.0。详见 [LICENSE](LICENSE)。
