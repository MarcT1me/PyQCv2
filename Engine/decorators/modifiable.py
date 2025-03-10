# decorators.py
from typing_extensions import cast

import Engine


# @deprecated("@modifiable temporarily broken")
def modifiable[T](
        *,
        is_class_method: bool = False,
        is_static_method: bool = False
) -> Engine.Callable[[Engine.Type[T]], Engine.Type[Engine.Modifiable[T]] | Engine.Type[T]]:
    """
    Class decorator that adds method 'modify' to change attributes in bulk

    Args:
        is_class_method: says that the modify method should be made class-bound
        is_static_method: says that the modify method should be made static

    Returns:
        new class
    """

    def decorator(cls: Engine.CLS) -> Engine.Modifiable[T]:

        if is_class_method:
            modify_wrapped = classmethod(Engine.Modifiable.modify)
        elif is_static_method:
            modify_wrapped = staticmethod(Engine.Modifiable.modify)
        else:
            modify_wrapped = Engine.Modifiable.modify

        setattr(cls, 'modify', modify_wrapped)
        return cast(Engine.Type[Engine.Modifiable[T]], cls)

    return decorator


if __name__ == "__main__":
    @modifiable()
    class Some:
        some: int = 1


    s = Some()
    print(s.some)  # 1
    s.modify(some=2)
    print(s.some)  # 2
