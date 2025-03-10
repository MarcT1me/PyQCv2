from typing_extensions import deprecated

import Engine
from Engine.decorators.classed_function import _ClassedFunction


@deprecated("Use only in the Engine, not recommended outside the Engine")
class _StorageFunction(_ClassedFunction):
    __is_storage__: bool = True

    def __init__(self, func, **attrs: Engine.KWARGS):
        self.__dict__.update(attrs)
        super().__init__(func)


def storage(**attrs: Engine.KWARGS) -> Engine.Callable[[Engine.FUNC], _StorageFunction]:
    def decorator(func: Engine.FUNC):
        return _StorageFunction(func, **attrs)

    return decorator
