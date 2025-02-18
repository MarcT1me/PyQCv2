from abc import abstractmethod

import Engine
from Engine.objects.scene_node.scene_node import SceneNode

from Engine.objects.ieventful import IEventful
from Engine.objects.iupdatable import IPreUpdatable, IUpdatable
from Engine.objects.irenderable import IPreRenderable, IRenderable


class SceneRoster(Engine.data.arrays.SimpleRoster):
    D2: dict[str, 'Engine.objects.SceneNode']
    D3: dict[str, 'Engine.objects.SceneNode']
    UI: dict[str, 'Engine.objects.SceneNode']


class Scene(SceneNode, IEventful, IPreUpdatable, IUpdatable, IPreRenderable, IRenderable):
    data: 'Engine.objects.SceneData'
    scene_type: Engine.DataType

    root_roster = SceneRoster(name="root")

    @abstractmethod
    def __init__(self, data: 'Engine.objects.SceneData'):
        super().__init__(data)
        self.roster = Engine.data.arrays.SimpleRoster(name=self.name)

    @abstractmethod
    def event(self, event: Engine.events.Event):
        ...

    @abstractmethod
    def pre_update(self):
        pass

    @abstractmethod
    def update(self):
        for child in self.children_ids.values():
            child.update()

    @abstractmethod
    def pre_render(self):
        pass

    @abstractmethod
    def render(self):
        for child in self.children_ids.values():
            if child:
                child.update()
