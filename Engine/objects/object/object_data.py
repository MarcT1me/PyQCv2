from dataclasses import dataclass
from typing import Optional

from Engine.objects.object_node.object_node_data import ObjectNodeData


@dataclass(kw_only=True)
class ObjectData(ObjectNodeData):
    priority: int = 0
    model: Optional[str] = None
