from functools import wraps
from typing import Any, Callable, Optional, cast
import inspect

import Engine


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
        if not hasattr(func, '__is_single_event_decorated__') and not already_single:
            raise TypeError(
                f"Function must be decorated {Engine.decorators.single_event} before using {window_event}"
            )

        # Checking the mandatory presence of the window parameter
        sig = inspect.signature(func)
        if 'window' not in sig.parameters:
            raise TypeError(f"Function {func} must have 'window' parameter to use {Engine.decorators.single_event}")

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Checking that the event is present in the arguments and getting her
            event = kwargs.get('event')

            if not event:
                raise ValueError("Event parameter not found in decorated function arguments")

            # Adding window to the arguments
            return func(*args, **{**kwargs, 'window': getattr(event, 'window', None)})

        wrapper.__is_window_event_decorated__ = True  # type: ignore

        return cast(Engine.FUNC, wrapper)

    return decorator(f) if f else decorator
