from functools import wraps
from typing import Any, Optional, cast
import inspect

import Engine


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

            return [func(*args, event=event, **kwargs) for event in Engine.App.instance.event.event_list]

        if not virtual:
            # Adding a marker for checking in other decorators
            wrapper.__is_single_event_decorated__ = True  # type: ignore
            return cast(Engine.FUNC, wrapper)
        else:
            func.__is_single_event_decorated__ = True
            return func

    return decorator(f) if f else decorator
