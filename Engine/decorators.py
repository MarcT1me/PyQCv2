from functools import wraps
from threading import Thread
from typing import Any
import Engine


def multithread(func):
    def wrapper(*args, **kwargs):
        Thread(target=lambda: func(*args, **kwargs)).start()

    return wrapper


def single_event(func):
    def wrapper(self):
        for event in Engine.app.App.event_list:
            with Engine.failures.Catch():
                func(self, event)

    return wrapper


def sdl_render(func):
    def wrapper(self):
        func(self)
        Engine.graphic.Graphics.flip()

    return wrapper


def gl_render(func):
    def wrapper(self):
        Engine.graphic.Graphics.context.clear(
            color=Engine.graphic.Graphics.gl_data.clear_color
        )
        func(self)
        Engine.graphic.Graphics.flip()

    return wrapper


def dev_only(func=None, *, _default: Any = None):
    """ Outer decorator taking the _default parameter. """

    def empty_func(*args, **kwargs):
        """ Placeholder function returning default value. """
        return _default

    def dev_only_decorator(func):
        """ Inner decorator altering wrapped function behavior based on the global flag. """

        @wraps(func)  # Preserve metadata for debugging and introspection
        def wrapper(*args, **kwargs):
            """ the final function """
            if Engine.data.Main.IS_RELEASE:
                return empty_func(*args, **kwargs)  # Return a placeholder function
            return func(*args, **kwargs)  # Normal function execution

        return wrapper

    return dev_only_decorator(func) if func else dev_only_decorator
