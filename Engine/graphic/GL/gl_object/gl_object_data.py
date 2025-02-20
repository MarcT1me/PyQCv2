from dataclasses import dataclass

import Engine


@dataclass(kw_only=True)
class GlObjectData(Engine.data.MetaData):
    binding: int = None
