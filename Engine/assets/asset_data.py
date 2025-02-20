from dataclasses import dataclass
from typing import Optional, Iterable
from enum import Enum

import Engine
from Engine.assets.asset_loader import AssetLoader


@dataclass
class AssetType:
    major: Engine.DataType
    minor: Enum = None

    @property
    def name(self) -> str:
        return f"{self.major.name}".replace("|", "")

    def __repr__(self):
        return (f"AssetType<{self.name}>("
                f"major: {self.major.name} "
                f"minor: {self.minor.name if self.minor else None})")


@dataclass(kw_only=True)
class AssetData(Engine.data.MetaData):
    type: AssetType = Engine.DataType.Asset
    dependencies: 'Optional[list[Engine.assets.LoadedAsset]]' = None
    content: Engine.T = None

    def __post_init__(self):
        if isinstance(self.type, Iterable):
            self.type = Engine.assets.AssetType(*self.type)
        elif isinstance(self.type, Engine.DataType):
            self.type = Engine.assets.AssetType(self.type)


class DefaultAssetLoader(AssetLoader):
    def load(self, asset_file: 'Engine.assets.AssetFileData') -> str | bytes:
        mode: str = "r" if asset_file.type & Engine.DataType.Text else "br"

        return asset_file.path.open(mode).read()

    def create(self, asset_file: 'Engine.assets.AssetFileData', dependencies: 'list[Engine.assets.LoadedAsset]',
               content: str | bytes) -> 'Engine.assets.AssetData':
        return AssetData(
            id=asset_file.id,
            dependencies=dependencies,
            content=content
        )
