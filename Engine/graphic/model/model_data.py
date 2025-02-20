from typing import Optional
from dataclasses import dataclass, field

import Engine


@dataclass(kw_only=True)
class ModelData(Engine.data.MetaData):
    mesh_id: Engine.data.Identifier = "default"
    model_type: Engine.data.Identifier = "static"

    lod_levels: list[Engine.data.Identifier] = field(default_factory=list)
    collision_mesh_id: Optional[Engine.data.Identifier] = None
