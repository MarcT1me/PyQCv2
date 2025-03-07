from typing import Any, Self, Tuple

import Engine
from Engine.decorators.storage import _StorageFunction


class _DeferrableFunction(_StorageFunction):
    _deferred_calls: list[Tuple[Engine.FUNC, Engine.ARGS, Engine.KWARGS, bool]]
    __is_deferred__: bool = True

    def __init__(self, func: Engine.FUNC, **attrs: Engine.KWARGS) -> Self:
        super().__init__(
            # function
            func,
            # attrs
            _deferred_calls=[],
            **attrs
        )

    def __call__(self, *args: Engine.ARGS, **kwargs: Engine.KWARGS) -> Any:
        # Сбрасываем очередь перед каждым вызовом функции
        self._deferred_calls.clear()
        ret = super().__call__(*args, **kwargs)
        self.do_defer()
        return ret

    def defer(self, func: Engine.FUNC, once=False, *args: Engine.ARGS, **kwargs: Engine.KWARGS) -> None:
        self._deferred_calls.append((func, args, kwargs, once))

    def do_defer(self) -> None:
        once_funcs = set()
        for func, args, kwargs, once in self._deferred_calls:
            if once and func in once_funcs:
                continue
            once_funcs.add(func)
            func(*args, **kwargs)


def deferrable(func: Engine.FUNC) -> _DeferrableFunction:
    return _DeferrableFunction(func)


class _ThreadSafeDeferrableFunction(_DeferrableFunction):
    _lock: 'Engine.threading.thread.Lock'
    __is_thread_safe__: bool = True

    def __init__(self, func) -> Self:
        super().__init__(
            # function
            func,
            # attrs
            _lock=Engine.threading.Thread.create_lock()
        )

    def defer(self, func: Engine.FUNC, once=False, *args: Engine.ARGS, **kwargs: Engine.KWARGS) -> None:
        with self._lock:
            super().defer(func, once, *args, **kwargs)

    def do_defer(self) -> None:
        with self._lock:
            super().do_defer()


def deferrable_threadsafe(func: Engine.FUNC) -> _ThreadSafeDeferrableFunction:
    return _ThreadSafeDeferrableFunction(func)
