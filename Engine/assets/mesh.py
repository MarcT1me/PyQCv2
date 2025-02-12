from dataclasses import dataclass, field
from typing import Optional

import Engine
from Engine.assets.asset_data import AssetData
from Engine.math import vec3


@dataclass(init=True)
class MeshData(AssetData):
    asset_type = Engine.DataType.Mesh
    vertices: list[vec3] = field(default_factory=list)
    indices: list[int] = field(default_factory=list)
    normals: list[vec3] = field(default_factory=list)

    lod_levels: list[str] = field(default_factory=list)
    material_slots: list[str] = field(default_factory=list)
    skeleton_id: Optional[str] = None

    collision_mesh_id: Optional[str] = None
