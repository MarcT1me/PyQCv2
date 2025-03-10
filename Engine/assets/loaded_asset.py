from typing import Any, final
from dataclasses import dataclass

import Engine


@dataclass(kw_only=True)
@final
class LoadedAsset:
    branch_id: Engine.data.Identifier
    id: Engine.data.Identifier

    @property
    def branch(self) -> 'Engine.assets.AssetRoster':
        return Engine.App.assets.storage.branch(self.branch_id.name)

    @property
    def asset_data(self) -> 'Engine.assets.AssetData':
        return self.branch[self.id]

    @property
    def content(self) -> Any:
        return self.asset_data.content

    def __repr__(self):
        return f"LoadedAsset<{self.id}>(branch_id: {self.branch_id})"
