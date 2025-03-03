from typing import Self

import Engine
from Engine.objects.scene_node.scene_node import SceneNode

from Engine.objects.ieventful import IEventful
from Engine.objects.iupdatable import IPreUpdatable, IUpdatable
from Engine.objects.irenderable import IPreRenderable, IRenderable


class Scene(SceneNode, IEventful, IPreUpdatable, IUpdatable, IPreRenderable, IRenderable):
    data: 'Engine.objects.SceneData'
    # SceneData
    multithread: bool
    is_critical_failures: bool

    node_heap: dict[Engine.data.Identifier, SceneNode] = {}

    def __init__(self, data: 'Engine.objects.SceneData'):
        super().__init__(data)
        self.scene_id = self.id
        Scene.node_heap[self.id] = self

    @staticmethod
    def add_node(value: SceneNode) -> None:
        Scene.node_heap[value.id] = value

    @staticmethod
    def get_node(identifier: Engine.data.Identifier) -> SceneNode:
        return Scene.node_heap.get(identifier, None)

    @staticmethod
    def pop_node(identifier: Engine.data.Identifier) -> SceneNode:
        return Scene.node_heap.pop(identifier, None)

    def add_child(self, value: Self) -> Self:
        self.add_node(value)
        self.children_ids.add(value.id)
        value.scene_id = self.scene_id
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
