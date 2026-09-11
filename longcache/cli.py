"""命令行入口：doctor / compress / list-models / bench / serve。"""
from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from longcache.config.loader import load_config
from longcache.core.logging import get_logger
from longcache.version import __version__, __description__

log = get_logger("longcache.cli")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="longcache",
        description=__description__,
    )
    p.add_argument("--version", action="version", version=f"longcache {__version__}")
    p.add_argument("--config", "-c", default=None,
                   help="配置文件路径（.json 或 .yaml）")
    sub = p.add_subparsers(dest="command")

    sub.add_parser("doctor", help="自检：加载模型卡 + KV 预算 + 稀疏注意力 + CED 推理冒烟")
    sub.add_parser("list-models", help="列出内置模型卡")

    cmp = sub.add_parser("compress", help="KV Cache 压缩预算模拟")
    cmp.add_argument("--context-len", type=int, default=1_048_576)
    cmp.add_argument("--budget-gb", type=float, default=1.0)

    b = sub.add_parser("bench", help="性能评测")
    b.add_argument("--steps", type=int, default=1000)

    s = sub.add_parser("serve", help="启动 FastAPI REST 服务")
    s.add_argument("--host", default=None)
    s.add_argument("--port", type=int, default=None)
    return p


def _cmd_doctor(cfg, args) -> int:
    from longcache.doctor import run_doctor
    return 0 if run_doctor(cfg) else 1


def _cmd_list_models(cfg, args) -> int:
    from longcache.models.loader import list_models
    for name in list_models():
        print(" -", name)
    return 0


def _cmd_compress(cfg, args) -> int:
    from longcache.kv.budget import simulate_budget
    simulate_budget(args.context_len, int(args.budget_gb * 1024 ** 3))
    return 0


def _cmd_bench(cfg, args) -> int:
    from longcache.benchmark.report import run_benchmark
    run_benchmark(cfg, args.steps)
    return 0


def _cmd_serve(cfg, args) -> int:
    from longcache.serving.app import run_server
    run_server(cfg, host=args.host, port=args.port)
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    cfg = load_config(args.config)

    if args.command is None:
        parser.print_help()
        return 0

    dispatch = {
        "doctor": _cmd_doctor,
        "list-models": _cmd_list_models,
        "compress": _cmd_compress,
        "bench": _cmd_bench,
        "serve": _cmd_serve,
    }
    try:
        return dispatch[args.command](cfg, args)  # type: ignore[operator]
    except Exception as e:  # noqa: BLE001
        log.error("命令失败：%s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
