from abc import ABC, abstractmethod
import Engine


class IEventful(ABC):
    @Engine.decorators.single_event(virtual=True)
    @abstractmethod
    def event(self, event: Engine.pg.event.Event): ...
