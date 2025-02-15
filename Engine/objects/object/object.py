from abc import abstractmethod
import Engine


class Object:
    data: 'Engine.objects.ObjectData'
    # MetaData
    id: str
    name: str
    # ObjectDdata
    is_active: bool
    position: Engine.math.vec3
    direction: Engine.math.vec3
    scale: Engine.math.vec3

    def __init__(self, data: 'Engine.objects.ObjectData'):
        self.data = data
        self.data.link_to_object(self)

    @Engine.decorators.single_event(virtual=TypeError)
    @abstractmethod
    def event(self, event: Engine.events.Event):
        ...

    @abstractmethod
    def update(self):
        ...
