from abc import abstractmethod


class IDestroyed:
    @abstractmethod
    def destroy(self): ...


class IReleasable:
    @abstractmethod
    def release(self): ...
