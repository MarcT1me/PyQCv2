from typing import Self

import Engine
from Engine.objects.scene_node.scene_node import SceneNode

from Engine.objects.ieventful import IEventful
from Engine.objects.iupdatable import IPreUpdatable, IUpdatable
from Engine.objects.irenderable import IPreRenderable, IRenderable


class Scene(SceneNode, IEventful, IPreUpdatable, IUpdatable, IPreRenderable, IRenderable):
    node_heap: dict[Engine.data.Identifier, SceneNode] = {}

    def __init__(self, data: 'Engine.objects.SceneNodeData'):
        super().__init__(data)
        self.data.scene_id = self.id
        Scene.node_heap[self.id] = self

    @staticmethod
    def add_node(value: SceneNode) -> None:
        Scene.node_heap[value.id] = value

    @staticmethod
    def get_node_identifier_from_name(name: str) -> 'Engine.data.Identifier | Engine.ResultType.NotFound':
        return next(
            filter(lambda _id: _id.name == name, Scene.node_heap),
            Engine.ResultType.NotFound
        )

    @staticmethod
    def get_node(identifier: Engine.data.Identifier) -> SceneNode:
        return Scene.node_heap.get(identifier, None)

    @staticmethod
    def pop_node(identifier: Engine.data.Identifier) -> SceneNode:
        return Scene.node_heap.pop(identifier, None)

    def add_child(self, value: Self) -> Self:
        self.add_node(value)
        self.data.children_ids.add(value.id)
        value.data.scene_id = self.data.scene_id
        return value

    def event(self, event: Engine.pg.event.Event):
        for child in self.iter_children():
            if child.is_eventful(): child.event(event)

    def pre_update(self):
        for child in self.iter_children():
            if child.is_pre_updatable(): child.pre_update()

    def update(self):
        for child in self.iter_children():
            if child.is_updatable(): child.update()

    def pre_render(self):
        for child in self.iter_children():
            if child.is_pre_renderable(): child.pre_render()

    def render(self):
        for child in self.iter_children():
            if child.is_renderable(): child.render()
