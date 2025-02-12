from typing import Any, Optional
from abc import ABC, abstractmethod

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
