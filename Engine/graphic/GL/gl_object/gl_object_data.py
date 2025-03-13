from dataclasses import dataclass, field

import Engine


@dataclass(kw_only=True)
class GlObjectData(Engine.data.MetaData):
    binding: int = field(default=None)
