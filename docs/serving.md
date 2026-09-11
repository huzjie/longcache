# REST 服务

## 启动

```bash
longcache serve --host 0.0.0.0 --port 8000
```

## 端点

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/health` `/healthz` | 健康检查 |
| GET | `/metrics` | 指标（计数器/仪表） |
| GET | `/v1/models` | 模型列表 |
| POST | `/v1/chat/completions` | 对话补全（OpenAI 兼容）|
| POST | `/v1/completions` | 文本补全（OpenAI 兼容）|

## 交互文档

启动后访问 `http://localhost:8000/docs` 查看 Swagger UI。
