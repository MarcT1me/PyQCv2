from abc import ABC
from typing import Optional
from dataclasses import dataclass, field

import Engine


@dataclass(kw_only=True)
class SceneNodeData(ABC, Engine.data.MetaData):
    parent_id: Optional[Engine.data.Identifier] = None
    children_ids: set[Engine.data.Identifier] = field(default_factory=set)
    scene_type: Engine.DataType = None
    scene_id: Engine.data.Identifier = None
