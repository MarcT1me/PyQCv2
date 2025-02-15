from functools import wraps
from typing import Any, Callable, Self, Optional, Type, cast
import inspect

import Engine


class _StorageFunction:
    def __init__(self, func, **attrs):
        self.func = func
        self.__dict__.update(attrs)
        wraps(func)(self)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


def with_store(**attrs: Any) -> Callable[[Engine.FUNC], _StorageFunction]:
    def decorator(func):
        return _StorageFunction(func, **attrs)

    return decorator


class _DeferrableFunction:
    def __init__(self, func) -> Self:
        self.func = func
        self.deferred_calls = []
        self.__is_deferred__ = True
        wraps(func)(self)

    def __call__(self, *args, **kwargs) -> Any:
        # Сбрасываем очередь перед каждым вызовом функции
        self.deferred_calls = []
        return self.func(*args, **kwargs)

    def defer(self, func: Callable, *args, **kwargs) -> None:
        self.deferred_calls.append((func, args, kwargs))

    def do_defer(self) -> None:
        while self.deferred_calls:
            func, args, kwargs = self.deferred_calls.pop(0)
            func(*args, **kwargs)


def deferrable(func: Engine.FUNC) -> _DeferrableFunction:
    return _DeferrableFunction(func)


class _ThreadSafeDeferrableFunction(_DeferrableFunction):
    def __init__(self, func) -> Self:
        super().__init__(func)
        self.lock = Engine.threading.Lock()

    def defer(self, func, *args, **kwargs) -> None:
        with self.lock:
            super().defer(func, *args, **kwargs)

    def do_defer(self) -> None:
        with self.lock:
            super().do_defer()


def deferrable_threadsafe(func: Engine.FUNC) -> _ThreadSafeDeferrableFunction:
    return _ThreadSafeDeferrableFunction(func)


def multithread(
        f: Optional[Engine.FUNC] = None,
        *,
        thread_class: Type[Engine.threading.Thread] = Engine.threading.Thread
) -> Callable[[Engine.FUNC], Engine.FUNC]:
    """ Multithread calling. New call = new thread"""

    def decorator(func: Engine.FUNC) -> Engine.FUNC:
        # Checking the mandatory presence of the event parameter
        sig = inspect.signature(func)
        has_thread = 'thread' in sig.parameters

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Engine.threading.Thread:
            if has_thread and 'thread' in kwargs:
                raise ValueError("Parameter 'thread' must not be passed explicitly with @multithread")

            # we pass the stream to the arguments if there is a place to
            action = lambda: func(*args, thread=thread, **kwargs) if has_thread else func(*args, **kwargs)

            # Creating an instance of the stream after defining the action
            thread = thread_class(action=action, daemon=True)
            thread.start()
            return thread

        return cast(Engine.FUNC, wrapper)

    # Processing for both @multithread and @multithread(...)
    return decorator(f) if f else decorator


def single_event(
        f: Optional[Engine.FUNC] = None,
        *,
        virtual=False) -> Engine.FUNC:
    """A decorator for automatic event handling. Requires the event parameter in the function."""

    def decorator(func):
        # Checking the mandatory presence of the event parameter
        sig = inspect.signature(func)
        if 'event' not in sig.parameters:
            raise TypeError(f"Function {func.__name__} must have 'event' parameter to use {single_event}")

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> list[Any]:
            if 'event' in kwargs:
                raise ValueError(f"Parameter 'event' must not be passed explicitly with {single_event}")

            return [func(*args, event=event, **kwargs) for event in Engine.App.event.event_list]

        # Adding a marker for checking in other decorators
        wrapper._is_single_event_decorated = True  # type: ignore

        return cast(Engine.FUNC, wrapper) if not virtual else func

    return decorator(f) if f else decorator


def window_event(
        f: Optional[Engine.FUNC] = None,
        *,
        already_single=False
) -> Callable[[Engine.FUNC], Engine.FUNC]:
    """
    A decorator for handling window events. Requires prior application of @single_event.

    Adds automatic transmission of the window parameter from the event.
    """

    def decorator(func):
        # checking for @single_event
        if not hasattr(func, '_is_single_event_decorated') and not already_single:
            raise TypeError(
                f"Function must be decorated {single_event} before using {window_event}"
            )

        # Checking the mandatory presence of the window parameter
        sig = inspect.signature(func)
        if 'window' not in sig.parameters:
            raise TypeError(f"Function {func} must have 'window' parameter to use {single_event}")

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Checking that the event is present in the arguments and getting her
            event = kwargs.get('event')

            if not event:
                raise ValueError("Event parameter not found in decorated function arguments")

            # Adding window to the arguments
            return func(*args, **{**kwargs, 'window': getattr(event, 'window', None)})

        wrapper._is_window_event_decorated = True  # type: ignore

        return cast(Engine.FUNC, wrapper)


    return decorator(f) if f else decorator


def updatable(cls: Engine.CLS) -> Engine.CLS:
    """Class decorator that adds static fields update capability

    Adds clas smethod 'update' to modify class attributes in bulk
    """

    def update(_, changes: dict[str, Any]) -> None:
        """Update multiple class attributes at once

        :param _: cls argument (class method required)
        :param changes: Dictionary of attribute_name -> new_value
        """
        for key, value in changes.items():
            setattr(cls, key, value)

    # Add as proper class method
    setattr(cls, 'update', classmethod(update))
    return cls


def sdl_render(func: Engine.FUNC) -> Engine.FUNC:
    """Decorator for SDL rendering. Automatically calls Graphics.flip()"""

    @wraps(func)
    def wrapper(self: Any) -> None:
        func(self)
        Engine.graphic.System.flip()

    return cast(Engine.FUNC, wrapper)


def gl_render(func: Engine.FUNC) -> Engine.FUNC:
    """Decorator for OpenGL rendering. Handles context clearing and buffer swap"""

    @wraps(func)
    def wrapper(self: Any) -> None:
        Engine.App.graphic.context.clear(color=Engine.app.App.graphic.gl_data.clear_color)
        func(self)
        Engine.graphic.System.flip()

    return cast(Engine.FUNC, wrapper)


def dev_only(
        f: Optional[Engine.FUNC] = None,
        *,
        _default: Any = None
) -> Callable[[Engine.FUNC], Engine.FUNC]:
    """Decorator to execute function only in development mode"""

    def decorator(func: Engine.FUNC) -> Engine.FUNC:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if Engine.data.MainData.IS_RELEASE:
                return _default
            return func(*args, **kwargs)

        return cast(Engine.FUNC, wrapper)

    return decorator(f) if f else decorator
