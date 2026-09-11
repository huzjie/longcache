"""配置加载器：支持 JSON（零依赖，必选）与 YAML（若安装 PyYAML）。"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from longcache.config.defaults import DEFAULT_CONFIG
from longcache.config.schema import RuntimeConfig
from longcache.core.errors import ConfigError


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """递归合并两个 dict，override 覆盖 base。"""
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(path: Optional[str] = None) -> RuntimeConfig:
    """从文件（或默认）加载运行时配置。

    path 支持 .json 与 .yaml/.yml。缺省返回默认配置。
    """
    raw: Dict[str, Any] = dict(DEFAULT_CONFIG)
    if path and Path(path).exists():
        p = Path(path)
        text = p.read_text(encoding="utf-8")
        try:
            if p.suffix.lower() == ".json":
                user = json.loads(text)
            else:
                import yaml  # type: ignore
                user = yaml.safe_load(text) or {}
        except ImportError:
            if p.suffix.lower() == ".json":
                user = json.loads(text)
            else:
                raise ConfigError(
                    f"读取 YAML 配置需要安装 PyYAML：pip install pyyaml（或改用 .json 配置）"
                )
        except Exception as e:  # noqa: BLE001
            raise ConfigError(f"解析配置失败 {p}: {e}")
        if not isinstance(user, dict):
            raise ConfigError(f"配置根节点必须是对象：{p}")
        raw = _deep_merge(raw, user)
    return RuntimeConfig.from_dict(raw)
