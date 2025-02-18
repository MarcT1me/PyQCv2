from abc import abstractmethod
import Engine


class IEventful:
    @abstractmethod
    @Engine.decorators.single_event(virtual=True)
    def event(self, event: Engine.pg.event.Event): ...
