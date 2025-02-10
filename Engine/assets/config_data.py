from dataclasses import dataclass

import Engine
from Engine.assets.asset_data import AssetData


@dataclass
class ConfigData(AssetData):
    asset_type = Engine.DataType.Config
    data: dict = None
