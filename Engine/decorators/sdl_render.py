from functools import wraps
from typing import Any, cast

import Engine


def sdl_render(func: Engine.FUNC) -> Engine.FUNC:
    """Decorator for SDL rendering. Automatically calls Graphics.flip()"""

    @wraps(func)
    def wrapper(self: Any) -> None:
        func(self)
        Engine.graphic.System.flip()

    return cast(Engine.FUNC, wrapper)
