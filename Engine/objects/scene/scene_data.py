from dataclasses import dataclass

from Engine.objects.scene_node.scene_node_data import SceneNodeData


@dataclass(init=True)
class SceneData(SceneNodeData):
    ...
