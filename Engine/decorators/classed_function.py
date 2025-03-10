from functools import wraps
from typing_extensions import deprecated, final

import Engine


@deprecated("Use only in the Engine, not recommended outside the Engine")
class _ClassedFunction:
    _func: Engine.FUNC
    __is_classed__: bool = True

    def __init__(self, func: Engine.FUNC):
        self._func = func
        wraps(func)(self)

    @final
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return wraps(self._func)(lambda *args, **kwargs: self(instance, *args, **kwargs))

    def __call__(self, *args: Engine.ARGS, **kwargs: Engine.KWARGS):
        return self._func(*args, **kwargs)


@deprecated("Use only in the Engine, not recommended outside the Engine")
def classed_function(func: Engine.FUNC) -> Engine.Callable[[Engine.FUNC], _ClassedFunction]:
    return _ClassedFunction(func)
