from abc import ABC, abstractmethod
from typing import Any, Optional, final, List
from pathlib import Path

import Engine


class AssetLoader(ABC):
    """ asset factory for the selected asset type """

    def __init__(self, asset_type: 'Engine.assets.AssetType'):
        """ Selecting the type of cassettes that the loader will respond to"""
        self.type: 'Engine.assets.AssetType' = asset_type

    @abstractmethod
    def load(
            self, asset_file: 'Engine.assets.AssetFileData'
    ) -> Any:
        """ The logic of loading data from a file """

    @abstractmethod
    def create(
            self, asset_file: 'Engine.assets.AssetFileData', dependencies: 'Optional[List[Engine.assets.LoadedAsset]]',
            content: Any
    ) -> 'Engine.assets.AssetData':
        """ The logic of processing previously uploaded data """

    @staticmethod
    @final
    def __read_text_file__(path: Path):
        """ reading text data from file """
        return path.open(mode="r").read()

    @staticmethod
    @final
    def __read_binary_file__(path: Path):
        """ reading binary data from file """
        return path.open(mode="br").read()
