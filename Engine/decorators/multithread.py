from functools import wraps
from typing import Any, Callable, Optional, Type, cast
import inspect

import Engine


def multithread(
        f: Optional[Engine.FUNC] = None,
        *,
        thread_class: Type['Engine.threading.Thread'] = None,
        daemon: bool = True,
        is_critical_failures: bool = None
) -> Callable[[Engine.FUNC], Engine.FUNC]:
    """ Multithread calling. New call = new thread"""
    thread_class = thread_class if thread_class else Engine.threading.Thread

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
            thread = thread_class(action=action, daemon=daemon, is_critical_failures=is_critical_failures)
            thread.start()
            return thread

        wrapper.__is_multithread_decorated__ = True

        return cast(Engine.FUNC, wrapper)

    # Processing for both @multithread and @multithread(...)
    return decorator(f) if f else decorator
