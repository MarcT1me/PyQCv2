from dataclasses import dataclass

import Engine
from Engine.assets.asset_data import AssetData


@dataclass(kw_only=True)
class TextureData(AssetData):
    type = Engine.DataType.Texture
    content: Engine.pg.Surface = None
