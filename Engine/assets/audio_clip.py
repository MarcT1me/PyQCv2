from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List

import Engine
from Engine.assets.asset_data import AssetData
from Engine.assets.asset_loader import AssetLoader


@dataclass(kw_only=True)
class AudioClipData(AssetData):
    type = Engine.DataType.AudioClip
    content: 'Engine.audio.Clip' = None


class AudioAssetLoader(AssetLoader):
    def load(self, asset_file: 'Engine.assets.AssetFileData') -> Path:
        return asset_file.path

    def create(self, asset_file: 'Engine.assets.AssetFileData',
               dependencies: 'Optional[List[Engine.assets.LoadedAsset]]', content: Path) -> 'Engine.assets.AssetData':
        return AudioClipData(
            id=asset_file.id,
            content=Engine.audio.Clip(content)
        )
