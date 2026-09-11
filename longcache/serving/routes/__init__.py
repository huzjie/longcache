"""路由注册。"""
from longcache.serving.routes.chat import router as chat_router
from longcache.serving.routes.completions import router as completions_router
from longcache.serving.routes.models import router as models_router
from longcache.serving.routes.health import router as health_router


def register_routes(app, cfg) -> None:
    app.include_router(health_router)
    app.include_router(models_router, prefix="/v1")
    app.include_router(chat_router, prefix="/v1")
    app.include_router(completions_router, prefix="/v1")
    # 存储 cfg 供路由使用
    app.state.cfg = cfg
    app.state.model = _load_model(cfg)


def _load_model(cfg):
    try:
        from longcache.models.loader import load_model
        return load_model(cfg.model)
    except Exception:  # noqa: BLE001
        return None
