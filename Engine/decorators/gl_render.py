from functools import wraps
from typing import Any, cast

import Engine


def gl_render(func: Engine.FUNC) -> Engine.FUNC:
    """Decorator for OpenGL rendering. Handles context clearing and buffer swap"""

    @wraps(func)
    def wrapper(self: Any) -> None:
        Engine.App.graphic.context.clear(color=Engine.app.App.graphic.gl_data.clear_color)
        func(self)
        Engine.graphic.System.flip()

    return cast(Engine.FUNC, wrapper)
