from dataclasses import dataclass, field

import Engine
from Engine.data import MetaData


@dataclass
class AssetData(MetaData):
    type: Engine.DataType = Engine.DataType.Asset
    dependencies: 'list[Engine.assets.LoadedAsset]' = field(default_factory=list)
    data: Engine.T = None
