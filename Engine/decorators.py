from functools import wraps
from typing import Any, Callable, Self, Optional, Type, TypeVar, cast, ClassVar
import inspect
import Engine

T = TypeVar('T', bound=Callable[..., Any])
CLS = TypeVar('CLS', bound=type)


def _update_wrapper_signature(
        wrapper: Callable,
        original: Callable,
        excluded_params: set[str]
) -> None:
    """Update wrapper signature by excluding specified parameters"""
    sig = inspect.signature(original)
    new_params = [
        p for p in sig.parameters.values()
        if p.name not in excluded_params
           and p.kind != inspect.Parameter.VAR_KEYWORD
    ]
    wrapper.__signature__ = sig.replace(parameters=new_params)


class _DeferrableFunction:
    def __init__(self, func) -> Self:
        self.func = func
        self.deferred_calls = []
        self.__is_deferred__ = True
        wraps(func)(self)

    def __call__(self, *args, **kwargs) -> Any:
        # Сбрасываем очередь перед каждым вызовом функции
        self.deferred_calls = []
        result = self.func(*args, **kwargs)
        return result

    def defer(self, func: Callable, *args, **kwargs) -> None:
        self.deferred_calls.append((func, args, kwargs))

    def do_defer(self) -> None:
        while self.deferred_calls:
            func, args, kwargs = self.deferred_calls.pop(0)
            func(*args, **kwargs)


def deferrable(func: Callable) -> _DeferrableFunction:
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


def deferrable_threadsafe(func: Callable) -> _ThreadSafeDeferrableFunction:
    return _ThreadSafeDeferrableFunction(func)


def multithread(
        f: Optional[T] = None,
        *,
        thread_class: Type[Engine.threading.Thread] = Engine.threading.Thread
) -> Callable[[T], T]:
    """ Multithread calling. New call = new thread"""

    def decorator(func: T) -> T:

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

        # Adjusting the signature
        if has_thread:
            _update_wrapper_signature(wrapper, func, {'thread'})

        return cast(T, wrapper)

    # Processing for both @multithread and @multithread(...)
    return decorator(f) if f else decorator


def single_event(func: T) -> T:
    """A decorator for automatic event handling. Requires the event parameter in the function."""

    # Checking the mandatory presence of the event parameter
    sig = inspect.signature(func)
    if 'event' not in sig.parameters:
        raise TypeError(f"Function {func.__name__} must have 'event' parameter to use {single_event}")

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> list[Any]:
        if 'event' in kwargs:
            raise ValueError(f"Parameter 'event' must not be passed explicitly with {single_event}")

        return [func(*args, event=event, **kwargs) for event in Engine.app.App.event_list]

    # Removing the event from the signature for external consumers
    _update_wrapper_signature(wrapper, func, {'event'})

    # Adding a marker for checking in other decorators
    wrapper._is_single_event_decorated = True  # type: ignore

    return cast(T, wrapper)


def window_event(func: T) -> T:
    """
    A decorator for handling window events. Requires prior application of @single_event.

    Adds automatic transmission of the window parameter from the event.
    """
    # checking for @single_event
    if not hasattr(func, '_is_single_event_decorated'):
        raise TypeError(
            f"Function must be decorated {single_event} before using {window_event}"
        )

    # Checking the mandatory presence of the window parameter
    sig = inspect.signature(func)
    if 'window' not in sig.parameters:
        raise TypeError(f"Function {func.__name__} must have 'window' parameter to use {single_event}")

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Checking that the event is present in the arguments and getting her
        event = kwargs.get('event')

        if not event:
            raise ValueError("Event parameter not found in decorated function arguments")

        # Adding window to the arguments
        return func(*args, **{**kwargs, 'window': getattr(event, 'window', None)})

    # changing signature for typing
    _update_wrapper_signature(wrapper, func, {'window'})

    wrapper._is_window_event_decorated = True  # type: ignore
    return cast(T, wrapper)


def updatable(cls: CLS) -> CLS:
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


def sdl_render(func: T) -> T:
    """Decorator for SDL rendering. Automatically calls Graphics.flip()"""

    @wraps(func)
    def wrapper(self: Any) -> None:
        func(self)
        Engine.graphic.Graphics.flip()

    _update_wrapper_signature(wrapper, func, set())
    return cast(T, wrapper)


def gl_render(func: T) -> T:
    """Decorator for OpenGL rendering. Handles context clearing and buffer swap"""

    @wraps(func)
    def wrapper(self: Any) -> None:
        Engine.graphic.Graphics.context.clear(color=Engine.graphic.Graphics.gl_data.clear_color)
        func(self)
        Engine.graphic.Graphics.flip()

    _update_wrapper_signature(wrapper, func, set())
    return cast(T, wrapper)


def dev_only(
        f: Optional[T] = None,
        *,
        _default: Any = None
) -> Callable[[T], T]:
    """Decorator to execute function only in development mode"""

    def decorator(func: T) -> T:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if Engine.data.Main.IS_RELEASE:
                return _default
            return func(*args, **kwargs)

        _update_wrapper_signature(wrapper, func, excluded_params=set())
        return cast(T, wrapper)

    return decorator(f) if f else decorator
