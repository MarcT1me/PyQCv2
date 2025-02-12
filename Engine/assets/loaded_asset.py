from typing import Any
from dataclasses import dataclass

import Engine


@dataclass
class LoadedAsset:
    branch_name: str
    id: str

    @property
    def branch(self) -> 'Engine.assets.AssetRoster':
        return Engine.app.App.assets.storage.branch(self.branch_name)

    @property
    def asset_data(self) -> 'Engine.assets.AssetData':
        return self.branch[self.id]

    @property
    def data(self) -> Any:
        return self.asset_data.data
