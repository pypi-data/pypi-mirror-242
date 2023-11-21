import abc
from types import ModuleType
from .plugin_system import Registry


class Api(ModuleType, abc.ABC):
    def __init__(self, globs, *args, **kwargs):
        super().__init__(__name__, *args, **kwargs)

        for k, v in globs.items():
            setattr(self, k, v)

        self.registry = Registry()
        self.host_plugin = self.register_plugin("host")

    def register_plugin(self, name: str):
        return self.registry.register_plugin(name)
