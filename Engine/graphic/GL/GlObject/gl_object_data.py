from dataclasses import dataclass

from Engine.data import MetaData


@dataclass(init=True)
class GlObjectData(MetaData):
    binding: int = 0
