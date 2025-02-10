from dataclasses import dataclass, field
from pathlib import Path

import Engine
from Engine.data import MetaData


@dataclass
class AssetFileData(MetaData):
    type: Engine.DataType = Engine.DataType.Asset
    dependencies: 'list[AssetFileData]' = field(default_factory=list)
    path: Path = None
