from dataclasses import dataclass
from typing import Optional

from Engine.objects.scene.scene_node_data import SceneNodeData


@dataclass(init=True)
class RenderMetaData(SceneNodeData):
    priority: int = 0
    model: Optional[str] = None
    is_visible: bool = True
