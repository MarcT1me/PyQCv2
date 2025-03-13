from typing_extensions import deprecated, Any, Self
from queue import Queue

import Engine
from Engine.decorators.classed_function import _ClassedFunction


@deprecated("Use only in the Engine, not recommended outside the Engine")
class _DeferrableFunction(_ClassedFunction):
    __is_deferred__: bool = True

    def __init__(self, func: Engine.FUNC) -> Self:
        super().__init__(func)
        self._deferred_calls: Queue[tuple[Engine.FUNC, Engine.ARGS, Engine.KWARGS]] = Queue()

    def __call__(self, *args: Engine.ARGS, **kwargs: Engine.KWARGS) -> Any:
        # Сбрасываем очередь перед каждым вызовом функции
        ret = super().__call__(*args, **kwargs)
        self.do_defer()
        return ret

    def defer(self,
              func: Engine.FUNC, *args: Engine.ARGS,
              **kwargs: Engine.KWARGS) -> None:
        self._deferred_calls.put((func, args, kwargs))

    def do_defer(self) -> None:
        while not self._deferred_calls.empty():
            func, args, kwargs = self._deferred_calls.get()
            func(*args, **kwargs)


def deferrable(func: Engine.FUNC) -> _DeferrableFunction:
    return _DeferrableFunction(func)


@deprecated("Use only in the Engine, not recommended outside the Engine")
class _ThreadSafeDeferrableFunction(_DeferrableFunction):
    _lock: 'Engine.threading.thread.Lock'
    __is_thread_safe__: bool = True

    def __init__(self, func) -> Self:
        super().__init__(func)
        self._lock = Engine.threading.Thread.create_lock()

    def defer(self,
              func: Engine.FUNC, *args: Engine.ARGS,
              **kwargs: Engine.KWARGS) -> None:
        with self._lock:
            super().defer(func, *args, **kwargs)

    def do_defer(self) -> None:
        with self._lock:
            super().do_defer()


def deferrable_threadsafe(func: Engine.FUNC) -> _ThreadSafeDeferrableFunction:
    return _ThreadSafeDeferrableFunction(func)
