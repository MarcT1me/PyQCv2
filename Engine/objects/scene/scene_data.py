from dataclasses import dataclass, field

from Engine.objects.scene_node.scene_node_data import SceneNodeData


@dataclass(kw_only=True)
class SceneData(SceneNodeData):
    multithread: bool = field(default=False)
    is_critical_failures: bool = field(default=True)
