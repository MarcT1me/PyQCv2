from functools import wraps
from typing import Any, Callable, Optional, cast

import Engine


def dev_only(
        f: Optional[Engine.FUNC] = None,
        *,
        _default: Any = None
) -> Callable[[Engine.FUNC], Engine.FUNC]:
    """Decorator to execute function only in development mode"""

    def decorator(func: Engine.FUNC) -> Engine.FUNC:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if Engine.data.MainData.IS_RELEASE:
                return _default
            return func(*args, **kwargs)

        return cast(Engine.FUNC, wrapper)

    return decorator(f) if f else decorator
