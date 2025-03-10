from functools import wraps
from typing_extensions import deprecated, Any, cast

import Engine


@deprecated("Has limited functionality, and there is a possibility to make a mistake. Use gl_render and her functions")
def sdl_render(func: Engine.FUNC) -> Engine.FUNC:
    """Decorator for SDL rendering. Automatically calls Graphics.flip()"""

    @wraps(func)
    def wrapper(self: Any) -> None:
        func(self)
        Engine.graphic.System.flip()

    wrapper.__is_sdl_render_decorated__ = False

    return cast(Engine.FUNC, wrapper)
