from dataclasses import dataclass
from typing import Optional, Iterable, List, final
from pathlib import Path

import Engine


@dataclass(kw_only=True)
@final
class AssetFileData(Engine.data.MetaData):
    type: 'Optional[Engine.assets.AssetType]' = None
    dependencies: 'Optional[List[AssetFileData]]' = None
    path: Path = None

    def __post_init__(self):
        if self.path:
            self.path = Path(self.path)
            self.id.name = self.path.name

            if not self.path.exists():
                raise FileNotFoundError(f"Asset file with id: `{self.id}`, path: `{self.path}` not found")

        if isinstance(self.type, Iterable):
            self.type = Engine.assets.AssetType(*self.type)
        elif isinstance(self.type, Engine.DataType):
            self.type = Engine.assets.AssetType(self.type)

    def __repr__(self):
        return f"AssetFileData<{self.id}>(type: `{self.type.name}`, path: `{self.path}`, deps: {self.dependencies})"

