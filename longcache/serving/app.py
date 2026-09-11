"""FastAPI 应用与启动入口。"""
from __future__ import annotations

from typing import Optional

from longcache.config.schema import RuntimeConfig
from longcache.core.logging import get_logger

log = get_logger("longcache.serving")


def create_app(cfg: Optional[RuntimeConfig] = None):
    """构建 FastAPI 应用。"""
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
    except ImportError as e:
        raise RuntimeError("需要安装 fastapi：pip install fastapi uvicorn") from e

    if cfg is None:
        from longcache.config.loader import load_config
        cfg = load_config()

    app = FastAPI(title="longcache", version="1.0.0",
                  description="超长上下文 MoE 推理引擎与 KV Cache 智能管理平台")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from longcache.serving.middleware import setup_middleware
    from longcache.serving.metrics import setup_metrics
    from longcache.serving.routes import register_routes

    setup_middleware(app)
    setup_metrics(app)
    register_routes(app, cfg)
    return app


def run_server(cfg: Optional[RuntimeConfig] = None, host: Optional[str] = None,
               port: Optional[int] = None) -> None:
    """启动 uvicorn 服务。"""
    try:
        import uvicorn
    except ImportError as e:
        raise RuntimeError("需要安装 uvicorn：pip install uvicorn") from e

    if cfg is None:
        from longcache.config.loader import load_config
        cfg = load_config()

    h = host or cfg.serving.host
    p = port or cfg.serving.port
    log.info("启动 longcache 服务 http://%s:%d （/docs 交互文档）", h, p)
    app = create_app(cfg)
    uvicorn.run(app, host=h, port=p, log_level="info")
