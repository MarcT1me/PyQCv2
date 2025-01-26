from dataclasses import dataclass
from typing import Optional

from Engine.objects.scene.scene_object_data import SceneObjectData


@dataclass(init=True)
class RenderMetaData(SceneObjectData):
    priority: int = 0
    model: Optional[str] = None
    is_visible: bool = True
