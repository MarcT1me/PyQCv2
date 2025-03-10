from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Any

import Engine
from Engine.assets.asset_data import AssetData
from Engine.assets.asset_loader import AssetLoader


@dataclass(kw_only=True)
class TextureData(AssetData):
    type = Engine.DataType.Texture
    content: Engine.pg.Surface = None


class TextureAssetLoader(AssetLoader):
    def load(self, asset_file: 'Engine.assets.AssetFileData') -> Path:
        return asset_file.path

    def create(self, asset_file: 'Engine.assets.AssetFileData',
               dependencies: 'Optional[List[Engine.assets.LoadedAsset]]', content: Any) -> 'Engine.assets.AssetData':
        return TextureData(
            id=asset_file.id,
            content=Engine.pg.image.load(content)
        )
