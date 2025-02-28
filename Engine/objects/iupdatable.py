from abc import abstractmethod


class IPreUpdatable:
    @abstractmethod
    def pre_update(self): ...


class IUpdatable:
    @abstractmethod
    def update(self): ...
