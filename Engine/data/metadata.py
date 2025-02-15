from uuid import uuid4
from dataclasses import dataclass, field
from typing import Optional, Self, Any


@dataclass
class MetaData:
    name: Optional[str] = None
    id: str = field(default_factory=uuid4)

    _linked_object: Any = field(init=False, default=None)

    def extern(self, changes: dict) -> Self:
        """ extern ths win_data and return new """
        [setattr(self, key, value) for key, value in changes.items()]
        return self

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        setattr(self._linked_object, key, value) if self._linked_object else Ellipsis

    def copy_to_object(self, obj):
        obj.__dict__.update(self.__dict__)

    def link_to_object(self, obj):
        setattr(self._linked_object, "__setattr__",
                lambda s, key, value: (super().__setattr__(key, value), setattr(s.data, key, value))
                )
        self._linked_object = obj
