"""指标：Prometheus 风格计数器（极简实现）。"""
from __future__ import annotations

import threading


class Metrics:
    """线程安全的简单计数器集合。"""

    def __init__(self):
        self._lock = threading.Lock()
        self._counters: dict = {}
        self._gauges: dict = {}

    def incr(self, name: str, n: int = 1) -> None:
        with self._lock:
            self._counters[name] = self._counters.get(name, 0) + n

    def set_gauge(self, name: str, value) -> None:
        with self._lock:
            self._gauges[name] = value

    def snapshot(self) -> dict:
        with self._lock:
            return {"counters": dict(self._counters), "gauges": dict(self._gauges)}


METRICS = Metrics()


def setup_metrics(app) -> None:
    """注册 /metrics 端点。"""
    @app.get("/metrics")
    async def metrics():
        return METRICS.snapshot()
