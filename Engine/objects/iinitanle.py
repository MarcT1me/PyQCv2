from abc import abstractmethod


class IPreInitable:
    @abstractmethod
    def __pre_init__(self): ...


class IPostInitable:
    @abstractmethod
    def __post_init__(self): ...
