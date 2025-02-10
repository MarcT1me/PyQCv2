from abc import ABC, abstractmethod

import Engine


class Loader(ABC):
    @abstractmethod
    def __call__(
            self, name: str, dependencies: 'list[Engine.assets.LoadedAsset]', content: str | bytes
    ) -> 'Engine.assets.AssetData': ...
