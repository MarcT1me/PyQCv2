from abc import ABC, abstractmethod


class IPreRenderable(ABC):
    @abstractmethod
    def pre_render(self): ...


class IRenderable(ABC):
    @abstractmethod
    def render(self): ...
