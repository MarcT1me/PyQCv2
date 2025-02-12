from dataclasses import dataclass, field
from typing_extensions import NamedTuple
from typing import Optional
from enum import Enum, auto

import Engine
from Engine.data import MetaData
from Engine.assets.asset_loader import AssetLoader


class MajorType(Enum):
    # file types
    Text = auto()
    Toml = auto()
    Json = auto()

    Bin = auto()
    Dill = auto()
    Pickle = auto()

    PyGame = auto()


class MinorType(Enum):
    # file encoding
    Asset = auto()
    Config = auto()
    Sav = auto()

    AudioClip = auto()
    VideoClip = auto()

    Shader = auto()
    Texture = auto()

    Model = auto()
    Mesh = auto()
    Material = auto()


class AssetType(NamedTuple):
    major: MajorType
    minor: MinorType
    tertiary: Optional[Enum] = None  # Опциональный параметр

    def get_name(self) -> str:
        base = f"{self.major.name}{self.minor.name}"
        if self.tertiary is not None:
            return f"{base}{self.tertiary.name}"
        return base


@dataclass
class AssetData(MetaData):
    type: Engine.DataType = Engine.DataType.Asset
    dependencies: 'Optional[list[Engine.assets.LoadedAsset]]' = None
    data: Engine.T = None


class DefaultAssetLoader(AssetLoader):
    def load(self, asset_file: 'Engine.assets.AssetFileData') -> str | bytes:
        mode: str = "r" if asset_file.type.major == MajorType.Text else "br"

        return asset_file.path.open(mode).read()

    def create(self, asset_file: 'Engine.assets.AssetFileData', dependencies: 'list[Engine.assets.LoadedAsset]',
               content: str | bytes) -> 'Engine.assets.AssetData':
        return AssetData(
            name=asset_file.name,
            dependencies=dependencies,
            data=content
        )
