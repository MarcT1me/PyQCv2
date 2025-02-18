from dataclasses import dataclass
from typing import Optional

import Engine
from Engine.objects.scene_node.scene_node_data import SceneNodeData


@dataclass(init=True)
class ObjectData(SceneNodeData):
    transform: 'Engine.data.Transform' = None
    flags: 'Engine.objects.ObjectFlags' = None
    priority: int = 0
    model: Optional[str] = None
