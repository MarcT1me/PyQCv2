from abc import abstractmethod

import Engine
from Engine.objects.object_node.object_node import ObjectNode

from Engine.objects.ieventful import IEventful
from Engine.objects.iupdatable import IUpdatable
from Engine.objects.irenderable import IPreRenderable


class Camera(ObjectNode, IEventful, IUpdatable, IPreRenderable):
    data: 'Engine.objects.CameraData'
    # CameraData
    camera_type: 'Engine.objects.CameraTypes'
    fov: int
    post_process: list[str]
    clip_planes: Engine.math.vec2
    
    @abstractmethod
    def __init__(self, data: 'Engine.objects.CameraData'):
        super().__init__(data)

    @abstractmethod
    @Engine.decorators.single_event(virtual=True)
    def event(self, event: Engine.pg.event.Event):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def pre_render(self):
        pass
