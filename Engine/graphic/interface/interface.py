from typing import Self
from abc import ABC, abstractmethod

import Engine
from Engine.objects.icontextmanager import IContextManager
from Engine.objects.ireleasable import IDestroyed, IReleasable


class Interface(ABC, IContextManager, IDestroyed, IReleasable):
    surface: Engine.pg.Surface

    def blit(self, *args, **kwargs):
        self.surface.blit(*args, **kwargs)

    @abstractmethod
    def __enter__(self) -> Self:
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        pass

    @abstractmethod
    def release(self):
        pass

    def destroy(self):
        pass
