from dataclasses import dataclass

import Engine
from Engine.assets.asset_data import AssetData


@dataclass
class AssetFileData(AssetData):
    path: str = None
    file_type: Engine.FileType = None
