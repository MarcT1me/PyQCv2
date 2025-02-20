from dataclasses import dataclass, field
from typing import Self

from Engine.data.identifier import Identifier


@dataclass(kw_only=True)
class MetaData:
    id: Identifier = field(default_factory=Identifier)

    def modify(self, changes: dict) -> Self:
        """ extern ths win_data and return new """
        [setattr(self, key, value) for key, value in changes.items()]
        return self

    def copy_to_object(self, obj):
        d = dict((key, attr) for key, attr in self.__dict__ if not key.startswith("__"))
        d.pop("copy_to_object")
        d.pop("link_to_object")
        obj.__dict__.update()
