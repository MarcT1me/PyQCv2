from dataclasses import dataclass
from typing import  Optional
from pathlib import Path

import Engine
from Engine.data import MetaData


@dataclass
class AssetFileData(MetaData):
    type: 'Engine.assets.AssetType' = None
    dependencies: 'Optional[list[AssetFileData]]' = None
    path: Path = None

    def __post_init__(self):
        self.path = Path(self.path)
        if not self.path.exists():
            raise FileNotFoundError(f"Asset file not found: {self.path}")
