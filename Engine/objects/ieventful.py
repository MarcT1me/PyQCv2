from abc import abstractmethod
import Engine


class IEventful:
    @Engine.decorators.single_event(virtual=True)
    @abstractmethod
    def event(self, event: Engine.pg.event.Event): ...
