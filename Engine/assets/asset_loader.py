from abc import ABC, abstractmethod
from typing import Any, Optional
from pathlib import Path

import Engine


class AssetLoader(ABC):
    def __init__(self, asset_type: 'Engine.assets.AssetType'):
        self.type: 'Engine.assets.AssetType' = asset_type

    @abstractmethod
    def load(
            self, asset_file: 'Engine.assets.AssetFileData'
    ) -> Any: ...

    @abstractmethod
    def create(
            self, asset_file: 'Engine.assets.AssetFileData', dependencies: 'Optional[list[Engine.assets.LoadedAsset]]',
            content: Any
    ) -> 'Engine.assets.AssetData': ...

    @staticmethod
    def __read_text_file__(path: Path):
        return path.open(mode="r").read()

    @staticmethod
    def __read_binary_file__(path: Path):
        return path.open(mode="br").read()
