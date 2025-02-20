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

    root_roster = SceneRoster()

    def __init__(self, data: 'Engine.objects.SceneData'):
        super().__init__(data)
        self.roster = Engine.data.arrays.SimpleRoster(name=self.id.name)
