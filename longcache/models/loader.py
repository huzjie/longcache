"""模型卡加载器：从内置 JSON 卡片读取。"""
from __future__ import annotations

import json
from pathlib import Path
from typing import List

from longcache.core.errors import ModelLoadError
from longcache.models.spec import ModelSpec

_CARDS_DIR = Path(__file__).resolve().parent / "cards"


def list_models() -> List[str]:
    """列出内置模型卡名（去扩展名）。"""
    if not _CARDS_DIR.exists():
        return []
    return sorted(p.stem for p in _CARDS_DIR.glob("*.json"))


def load_model(name: str) -> ModelSpec:
    """按名字加载模型卡。"""
    path = _CARDS_DIR / f"{name}.json"
    if not path.exists():
        raise ModelLoadError(f"模型卡不存在：{name}（可用：{list_models()}）")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        raise ModelLoadError(f"解析模型卡失败 {path}: {e}")
    return ModelSpec.from_dict(data)


def load_all_models() -> List[ModelSpec]:
    return [load_model(n) for n in list_models()]
