from abc import ABC
from typing import Optional
from dataclasses import dataclass, field

import Engine


@dataclass(kw_only=True)
class SceneNodeData(ABC, Engine.data.MetaData):
    scene_id: Optional[Engine.data.Identifier] = field(default=None)
    parent_id: Optional[Engine.data.Identifier] = field(default=None)
    children_ids: set[Engine.data.Identifier] = field(default_factory=set)
