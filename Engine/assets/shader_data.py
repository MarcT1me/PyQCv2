from dataclasses import dataclass

import Engine
from Engine.assets.asset_data import AssetData


@dataclass
class ShaderData(AssetData):
    asset_type = Engine.DataType.Shader
    data: str = None
    shader_type: Engine.ShaderType = None
