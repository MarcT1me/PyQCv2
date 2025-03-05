from abc import ABC
from typing import Optional, Self, Iterator

import Engine

from Engine.objects.ieventful import IEventful
from Engine.objects.iupdatable import IPreUpdatable, IUpdatable
from Engine.objects.irenderable import IPreRenderable, IRenderable


class SceneNode(ABC, Engine.data.MetaObject):
    data: 'Engine.objects.SceneNodeData'
    # SceneNodeData
    parent_id: Optional[Engine.data.Identifier]
    children_ids: set[Engine.data.Identifier]
    scene_id: Engine.data.Identifier

    def __init__(self, data: 'Engine.objects.SceneNodeData'):
        super().__init__(data)

    @property
    def scene(self) -> 'Engine.objects.Scene':
        return Engine.objects.Scene.get_node(self.data.scene_id)

    def add_child(self, value: Self) -> Self:
        self.data.children_ids.add(value.data.id)
        self.scene.add_node(value)
        value.data.scene_id = self.data.scene_id
        return value

    def get_child_identifier_from_name(self, name: str) -> 'Engine.data.Identifier | Engine.ResultType.NotFound':
        return next(
            filter(lambda _id: _id.name == name, self.data.children_ids),
            Engine.ResultType.NotFound
        )

    def iter_children_ids(self):
        for child_id in self.data.children_ids:
            yield child_id

    def iter_children(self) -> Iterator[Self]:
        for child_id in self.iter_children_ids():
            yield Engine.objects.Scene.get_node(child_id)

    def pop_child(self, identifier: Engine.data.Identifier) -> None:
        self.data.children_ids.remove(identifier)
        return self.scene.pop_node(identifier)

    @property
    def parent(self) -> Self:
        return self.scene.get_node(self.parent_id)

    def link_to_parent(self, parent_id: Engine.data.Identifier) -> Self:
        if self.parent:
            self.unlink_parent()
        parent = self.scene.get_node(parent_id)
        parent.data.children_ids.add(self.id)
        self.data.parent_id = parent.data.id
        return parent

    def unlink_parent(self):
        if self.parent:
            self.parent.data.children_ids.remove(self.id)
            self.data.parent_id = None

    def is_eventful(self):
        return isinstance(self, IEventful)

    def is_pre_updatable(self):
        return isinstance(self, IPreUpdatable)

    def is_updatable(self):
        return isinstance(self, IUpdatable)

    def is_pre_renderable(self):
        return isinstance(self, IPreRenderable)

    def is_renderable(self):
        return isinstance(self, IRenderable)
