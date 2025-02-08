from dataclasses import dataclass, field

import Engine
from Engine.data import MetaData


@dataclass(init=True)
class AssetData(MetaData):
    asset_type: Engine.DataType = Engine.DataType.Asset
    dependencies: list[str] = field(default_factory=list)
