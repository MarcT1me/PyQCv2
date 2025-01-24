from functools import wraps
from typing import Any
import Engine


def updatable(cls):
    # Define the update method inside the decorator
    def update(_, changes: dict) -> None:
        for key, value in changes.items():
            setattr(cls, key, value)

    # Set the update method as a class method
    setattr(cls, 'update', classmethod(update))
    return cls


def multithread(func):
    def wrapper(*args, **kwargs):
        Engine.threading.Thread(
            action=lambda: func(*args, **kwargs),
            daemon=True
        ).start()

    return wrapper


def single_event(func):
    def wrapper(self):
        for event in Engine.app.App.event_list:
            with Engine.failures.Catch(identifier=f"{single_event}_Catch__ENGINE__"):
                func(self, event)

    wrapper._is_single_event_decorated = True
    return wrapper


def window_event(func):
    if not hasattr(func, '_is_single_event_decorated'):
        raise TypeError(f"Function must be decorated {single_event} before  using {window_event}")

    def wrapper(self, event):
        func(self, event, getattr(event, 'window', None))

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

    def dev_only_decorator(func):
        """ Inner decorator altering wrapped function behavior based on the global flag. """

        @wraps(func)  # Preserve metadata for debugging and introspection
        def wrapper(*args, **kwargs):
            """ the final function """
            if Engine.data.Main.IS_RELEASE:
                return _default  # Return a placeholder function
            return func(*args, **kwargs)  # Normal function execution

        return wrapper

    return dev_only_decorator(func) if func else dev_only_decorator
