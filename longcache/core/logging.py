"""日志初始化。提供统一的 get_logger。"""
from __future__ import annotations

import logging
import sys

_FMT = "%(asctime)s %(levelname)-7s %(name)s - %(message)s"


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """返回一个配置好的 logger，重复调用幂等。"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter(_FMT))
        logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
    return logger
