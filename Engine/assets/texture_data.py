from dataclasses import dataclass

import Engine
from Engine.assets.asset_data import AssetData


@dataclass
class TextureData(AssetData):
    asset_type = Engine.DataType.Texture
    data: Engine.pg.Surface = None
