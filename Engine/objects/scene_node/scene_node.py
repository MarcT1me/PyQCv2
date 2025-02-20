from abc import ABC
from typing import Optional, Self

import Engine


class SceneNode(ABC, Engine.data.MetaObject):
    data: 'Engine.objects.SceneNodeData'
    # SceneNodeData
    parent_id: Optional[Engine.data.Identifier]
    children_ids: set[Engine.data.Identifier]
    scene_type: Engine.DataType
    scene_id: Engine.data.Identifier

    def __init__(self, data: 'Engine.objects.SceneNodeData'):
        super().__init__(data)

    @staticmethod
    def root_roster() -> 'Engine.objects.SceneRoster':
        return Engine.objects.Scene.root_roster

    @staticmethod
    def get_node(node_id: Engine.data.Identifier) -> 'SceneNode':
        return SceneNode.root_roster()[node_id]

    @property
    def scene_branch(self) -> dict[str, Self]:
        return self.root_roster().branch(self.scene_type.name)

    @property
    def scene(self) -> 'Engine.objects.Scene':
        return self.scene_branch[self.scene_id]

    def iter_children(self):
        for child_id in self.children_ids:
            yield self.scene.roster[child_id]

    def add_child(self, value: Self) -> None:
        self.children_ids.add(value.id)
        self.scene.add_child(value)

    def remove_child(self, identifier: Engine.data.Identifier) -> None:
        self.children_ids.remove(identifier)
        self.scene.remove_child(identifier)

    @property
    def parent(self) -> 'Engine.objects.SceneData':
        return self.root_roster()[self.parent_id]

    def link_to_parent(self, parent_id: Engine.data.Identifier):
        if self.parent:
            self.unlink_parent()
        parent = self.get_node(parent_id)
        parent.children_ids.add(self.id)
        self.parent_id = parent.data.id

    def unlink_parent(self):
        parent: Engine.objects.SceneNode = self.parent
        if not parent:
            parent.children_ids.remove(self.id)
            self.parent_id = None
