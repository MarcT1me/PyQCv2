from dataclasses import dataclass

from Engine.objects.scene_node.scene_node_data import SceneNodeData


@dataclass(kw_only=True)
class SceneData(SceneNodeData):
    ...
