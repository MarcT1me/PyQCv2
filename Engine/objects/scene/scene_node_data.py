from dataclasses import dataclass, field
from typing import Optional, Self

import Engine.objects
from Engine.objects.object.object_data import ObjectData


@dataclass(init=True)
class SceneNodeData(ObjectData):
    scene_id: str = None
    parent_id: Optional[str] = None
    children_ids: dict[str, Self] = field(default_factory=dict)

    def add_child(self, value: Self) -> None:
        self.children_ids[value.id] = value

    def remove_child(self, _id: str) -> None:
        del self.children_ids[_id]

    def link_to_parent(self, branch_type: Engine.DataType, parent_id: str):
        obj: Engine.objects.SceneNode = Engine.objects.Scene.roster.branch(branch_type.name)[parent_id]
        obj.data.children_ids[self.id] = self
        self.parent_id = obj.data.id
