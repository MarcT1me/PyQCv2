import Engine


def modifiable(
        cls: Engine.CLS = None,
        *,
        is_class_method: bool = False,
        is_static_method: bool = False
) -> Engine.CLS:
    """
    Class decorator that adds method 'modify' to change attributes in bulk

    Keyword Args:
        is_class_method: says that the modify method should be made class-bound
        is_static_method: says that the modify method should be made static

    Returns:
        new class
    """

    def decorator(c: Engine.CLS) -> Engine.FUNC:
        def modify(obj: Engine.T, **changes: Engine.KWARGS) -> Engine.T:
            """
            Update multiple class attributes at once

            Args:
                obj: cls or self argument
                changes: kwargs dictionary of new values - {item: new_value}

            Returns:
                current object after modifying

            Raises:
                AttributeError: if one of kwarg argument to change not in object
            """
            for item, value in changes.items():
                if hasattr(obj, item):
                    setattr(obj, item, value)
                else:
                    AttributeError("Cant set an undescribed attribute")
            return obj

        # Add as proper class method
        setattr(
            c, 'update',
            classmethod(modify) if is_class_method else \
                staticmethod(modify) if is_static_method else \
                    modify
        )

        return cls

    return decorator(cls) if cls else decorator
