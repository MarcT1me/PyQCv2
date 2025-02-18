from typing import Optional, Self
from abc import ABC

import Engine


class SceneNode(ABC, Engine.data.MetaObject):
    data: 'Engine.objects.SceneNodeData'
    # SceneNodeData
    scene_type: Engine.DataType = None
    parent_id: Optional[str]
    children_ids: dict[str, Self]

    def __init__(self, data: 'Engine.objects.SceneNodeData'):
        super().__init__(data)

    @property
    def scene_branch(self) -> dict[str, Self]:
        return Engine.objects.Scene.roster.branch(self.scene_type.name)

    def from_id(self, object_id: str):
        return self.scene_branch[object_id]

    def iter_children(self, func_name: str, *args, **kwargs):
        for child_id in self.children_ids.values():
            self.from_id(child_id).__getattribute__(func_name)(*args, **kwargs)

    def add_child(self, value: Self) -> None:
        self.children_ids[value.id] = value

    def remove_child(self, _id: str) -> None:
        del self.children_ids[_id]

    def link_to_parent(self, scene_type: Engine.DataType, parent_id: str):
        obj: Engine.objects.SceneNode = Engine.objects.Scene.roster.branch(scene_type.name)[parent_id]
        obj.data.children_ids[self.id] = self
        self.parent_id = obj.data.id
