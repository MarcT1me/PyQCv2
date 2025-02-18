from abc import abstractmethod


class IPreRenderable:
    @abstractmethod
    def pre_render(self): ...


class IRenderable:
    @abstractmethod
    def render(self): ...
