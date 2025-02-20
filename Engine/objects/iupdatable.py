from abc import ABC, abstractmethod


class IPreUpdatable(ABC):
    @abstractmethod
    def pre_update(self): ...


class IUpdatable(ABC):
    @abstractmethod
    def update(self): ...
