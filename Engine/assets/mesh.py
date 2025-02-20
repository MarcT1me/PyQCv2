from dataclasses import dataclass, field
from typing import Optional

import Engine
from Engine.assets.asset_data import AssetData


@dataclass(kw_only=True)
class MeshData(AssetData):
    type = Engine.DataType.Mesh
    content: 'list[Engine.graphic.GL.VertexAttributes]' = field(default_factory=list)
    indices: list[int] = field(default_factory=list)
    skeleton: Optional = None

    material_slots: list[Engine.data.Identifier] = field(default_factory=list)
