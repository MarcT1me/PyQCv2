from functools import wraps
from typing import Any, cast

import Engine


def gl_render(func: Engine.FUNC) -> Engine.FUNC:
    """Decorator for OpenGL rendering. Handles context clearing and buffer swap"""
    if not Engine.data.MainData.IS_USE_GL:
        raise BrokenPipeError("Cant use gl_render without MainData.IS_USE_GL (check settings.engconf)")

    @wraps(func)
    def wrapper(self: Any) -> None:
        Engine.App.graphic.context.clear(color=Engine.app.App.graphic.gl_data.clear_color)
        func(self)
        Engine.graphic.System.flip()

    wrapper.__is_gl_render_decorated__ = False

    return cast(Engine.FUNC, wrapper)
