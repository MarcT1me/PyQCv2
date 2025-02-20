from dataclasses import dataclass

from Engine.objects.scene_node.scene_node_data import SceneNodeData
from Engine.data.transform import Transform
from Engine.objects.object.object_flags import ObjectFlags


@dataclass(kw_only=True)
class ObjectNodeData(SceneNodeData):
    transform: Transform = None
    flags: ObjectFlags = None
