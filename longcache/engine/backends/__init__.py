"""推理后端：mock / vllm / sglang / ollama（可插拔）。"""
from longcache.engine.backends.base import Backend
from longcache.engine.backends.mock import MockBackend
from longcache.core.registry import Registry

BackendRegistry = Registry("backend")


def _register_defaults():
    from longcache.engine.backends.vllm import VLLMBackend
    from longcache.engine.backends.sglang import SGLangBackend
    from longcache.engine.backends.ollama import OllamaBackend
    BackendRegistry.register("vllm")(VLLMBackend)
    BackendRegistry.register("sglang")(SGLangBackend)
    BackendRegistry.register("ollama")(OllamaBackend)
    BackendRegistry.register("mock")(MockBackend)


_register_defaults()


def get_backend(name: str) -> Backend:
    try:
        return BackendRegistry.get(name)()
    except KeyError:
        raise ValueError(f"未知后端 {name!r}，可用：{BackendRegistry.keys()}")


__all__ = ["Backend", "BackendRegistry", "get_backend"]
