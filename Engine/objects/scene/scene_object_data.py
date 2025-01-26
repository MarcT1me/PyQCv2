from dataclasses import dataclass, field
from typing import Optional

from Engine.objects.object.object_data import ObjectData


@dataclass(init=True)
class SceneObjectData(ObjectData):
    parent: Optional[str] = None
    children: dict[str, 'SceneObjectData'] = field(default_factory=dict)

    def add_child(self, value: 'SceneObjectData') -> None:
        self.children[value.id] = value

    def remove_child(self, _id: str) -> None:
        del self.children[_id]
