from typing import Self
from dataclasses import dataclass, field

import Engine
from Engine.data.identifier import Identifier


@dataclass(kw_only=True)
@Engine.decorators.modifiable()
class MetaData:
    id: Identifier = field(default_factory=Identifier)

    def modify(self, **changes: Engine.KWARGS) -> Self:
        """
        Update multiple class attributes at once

        Args:
            changes: kwargs dictionary of new values - {item: new_value}

        Returns:
            current object after modifying

        Raises:
            AttributeError: if one of kwarg argument to change not in object
        """

    def __copy_to_object__(self, obj):
        d = dict((key, attr) for key, attr in self.__dict__ if not key.startswith("__"))
        d.pop("modify")
        obj.__dict__.update()
