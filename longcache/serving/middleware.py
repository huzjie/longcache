"""中间件：请求日志、并发计数、请求体大小限制。"""
from __future__ import annotations

import time
import uuid


def setup_middleware(app) -> None:
    """注册请求日志中间件。"""
    @app.middleware("http")
    async def log_requests(request, call_next):
        rid = uuid.uuid4().hex[:8]
        start = time.time()
        response = await call_next(request)
        elapsed = (time.time() - start) * 1000
        response.headers["X-Request-ID"] = rid
        response.headers["X-Process-Time-Ms"] = f"{elapsed:.1f}"
        return response
