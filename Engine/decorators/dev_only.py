from functools import wraps
from typing_extensions import deprecated, Optional, Any, cast

import Engine


@deprecated("Use only in development. Recommended remove all functions marked that @dev_only in the release.")
def dev_only(
        f: Optional[Engine.FUNC] = None,
        *,
        _default: Any = None
) -> Engine.FUNC | Engine.Callable[[Engine.FUNC], Engine.FUNC]:
    """Decorator to execute function only in development mode"""

    def decorator(func: Engine.FUNC) -> Engine.FUNC:
        @wraps(func)
        def wrapper(*args: Engine.ARGS, **kwargs: Engine.KWARGS) -> Any:
            if Engine.data.MainData.IS_RELEASE:
                return _default
            return func(*args, **kwargs)

        wrapper.__is_dev_only_decorated__ = False

        return cast(Engine.FUNC, wrapper)

    return decorator(f) if f else decorator
