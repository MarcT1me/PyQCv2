from typing_extensions import Self, deprecated
from loguru import logger

import Engine
from Engine.graphic.interface.interface import Interface


@deprecated("Has limited functionality, and there is a possibility to make a mistake. Use other interface class")
class SdlInterface(Interface):
    def __init__(self) -> None:
        self.surface = Engine.pg.Surface(
            Engine.App.graphic.window.data.size
        )

    def __str__(self):
        return f"SdlInterface<>(size: {Engine.math.vec2(self.surface.get_size())})"

    def __enter__(self) -> Self:
        self.surface.fill((0, 0, 0))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> False:
        self.__render__()
        return False

    def __render__(self):
        Engine.App.graphic.window.blit(self.surface, (0, 0))

    def release(self):
        logger.info("Interface released")
