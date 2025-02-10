from typing_extensions import NamedTuple
from pathlib import Path

import Engine
from Engine.assets.loader import Loader


class _AssetRoster(Engine.arrays.Roster):
    def __init__(self, name: str, directory: str | None, loader: Engine.CLS | None):
        super().__init__(name, branch_type=_AssetRoster)
        self.directory = directory
        self.loader = loader

    def new_asset_branch(self, name: str, directory: str | None, loader: Engine.CLS | None):
        return self.new_branch(name, directory, loader)


class _AssetLoader(Loader):
    def __call__(
            self, name: str, dependencies: 'list[Engine.assets.LoadedAsset]', content: str | bytes
    ) -> 'Engine.assets.AssetData':
        return Engine.assets.AssetData(
            name=name,
            dependencies=dependencies,
            data=content
        )


class AssetTypeConfig(NamedTuple):
    directory: Path
    loader: 'Engine.assets.Loader'


class Manager(_AssetRoster):
    def __init__(self, root_dir: Path, asset_configs: dict[str, AssetTypeConfig]):
        super().__init__("root", root_dir, _AssetLoader())

        for name, config in asset_configs.items():
            self.new_asset_type(name, config.directory, config.loader)

    @staticmethod
    def get_branch(asset_type: Engine.DataType) -> _AssetRoster:
        raise NotImplemented()

    def load(self, asset_file: 'Engine.assets.AssetFileData'):
        dependencies: list[Engine.assets.LoadedAsset] = []
        for dependency in asset_file.dependencies:
            dependencies.append(self.load(dependency))

        mode = "rb" if asset_file.type & Engine.DataType.Binary else "r"
        with asset_file.path.open(mode) as f:
            content: str | bytes = f.read()

        branch: _AssetRoster = self.get_branch(asset_file.type)
        obj: Engine.assets.AssetData = branch.loader(asset_file.name, dependencies, content)
        branch[obj.id] = obj

        return Engine.assets.LoadedAsset(branch.name, obj.id)
