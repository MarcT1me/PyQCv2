from dataclasses import dataclass
from pathlib import Path

import Engine
from Engine.assets.asset_data import AssetData
from Engine.assets.asset_loader import AssetLoader


@dataclass
class AudioClipData(AssetData):
    asset_type = Engine.DataType.AudioClip
    data: 'Engine.audio.Clip' = None


class AudioAssetLoader(AssetLoader):
    def load(self, asset_file: 'Engine.assets.AssetFileData') -> Path:
        return asset_file.path

    def create(self, asset_file: 'Engine.assets.AssetFileData', dependencies: 'list[Engine.assets.LoadedAsset]',
               content: Path) -> 'Engine.assets.AssetData':
        return AudioClipData(
            name=asset_file.name,
            data=Engine.audio.Clip(content)
        )
