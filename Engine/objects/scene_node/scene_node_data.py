from dataclasses import dataclass, field
from typing import Optional, Self

import Engine
from Engine.data import MetaData


@dataclass(init=True)
class SceneNodeData(MetaData):
    parent_id: Optional[str] = None
    children_ids: dict[str, Self] = field(default_factory=dict)

    scene_type: Engine.DataType = None
