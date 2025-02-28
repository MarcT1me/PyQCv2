from typing import Dict, Set, Any, final
from pprint import pformat
from loguru import logger

import Engine


class AssetError(Exception):
    """Base class for all asset loading exceptions"""


@final
class AssetRoster(Engine.data.arrays.Roster):
    def __init__(self, name: str, loader: 'Engine.assets.Loader | None', *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.loader = loader

    def definite(self, name) -> 'Engine.assets.AssetData':
        for asset in self.values():
            if asset.id.name == name:
                return asset
        raise AssetError(f"Cant find definite asset with name {name}")


class CyclicDependencyError(AssetError):
    pass


class MissingDependencyError(AssetError):
    pass


@final
class DependencyResolver:
    def __init__(self, loading_func: Engine.FUNC):
        self.loading_func = loading_func
        self._loading_stack: Set[str] = set()

    def resolve(self, asset_file: 'Engine.assets.AssetFileData') -> 'Set[Engine.assets.LoadedAsset]':
        """
        Retrieves the list of downloaded dependencies for the specified cassette
        with loop handling and caching
        """
        dependencies = []

        if asset_file.dependencies is None:
            return dependencies
        else:
            logger.info(f"DependencyResolver - loading dependencies for {asset_file.id}\n")
            cache_key = str(asset_file.path)

            # Checking cycles
            if cache_key in self._loading_stack:
                raise CyclicDependencyError(
                    f"Cyclic dependency detected: {asset_file.path}"
                )

            with Engine.threading.Thread.global_lock:
                self._loading_stack.add(cache_key)

            try:
                # Recursively loading all dependencies
                dependencies = [self.loading_func(dep) for dep in asset_file.dependencies]
            except Exception as e:
                raise AssetError(f"Failed to load asset {asset_file.id}") from e
            finally:
                with Engine.threading.Thread.global_lock:
                    self._loading_stack.remove(cache_key)

            logger.success(
                f"DependencyResolver - Dependencies for {asset_file.id} loaded:\n"
                f"deps:\n"
                f"{pformat(dependencies)}\n"
            )

        return dependencies


class InvalidAssetTypeError(AssetError):
    pass


class DuplicatedAssetTypeConfig(AssetError):
    pass


@final
class AssetManager:
    def __init__(self, asset_loaders: 'list[Engine.assets.AssetLoader]'):
        # Initializing the root Roster
        self.storage: AssetRoster[str, AssetRoster[str, Engine.assets.AssetData]] = AssetRoster(
            name="root", loader=None
        )
        self._dependency_resolver = DependencyResolver(self.load)

        # Registering asset types as branches in the Roster
        self._register_asset_type(asset_loaders)

        logger.success("AssetManager - init")

    def _register_asset_type(self, asset_loaders: 'list[Engine.assets.AssetLoader]'):
        asset_types: Dict[str, Engine.assets.AssetLoader] = {}

        for loader in asset_loaders:
            name = loader.type.name
            if not loader:
                raise InvalidAssetTypeError("Loader not configured")
            elif name in asset_types:
                raise DuplicatedAssetTypeConfig(f"Asset type '{name}' already registered")

            logger.info(
                f"Register asset type:\n"
                f"logger: {loader}\n"
                f"type {loader.type}"
            )
            # Creating a new branch in the Roster
            self.storage.new_branch(
                name=name,
                loader=loader
            )

            # Saving the config for quick access
            asset_types[name] = loader

        print()

    def get_branch(self, branch_name: str) -> AssetRoster:
        # We are looking for a branch by type name in the root Roster
        branch = self.storage.branch(branch_name)
        if branch is not None:
            return branch
        raise InvalidAssetTypeError(f"No branch with name {branch_name}")

    def load(
            self, asset_file: 'Engine.assets.AssetFileData', *,
            loaded_dependencies: 'list[Engine.assets.LoadedAsset]' = []
    ) -> 'Engine.assets.LoadedAsset':
        try:
            logger.info(
                f"AssetManager - Loading asset:\n"
                f"id: {asset_file.id}" + str(
                    f"\npath: {asset_file.path}" if asset_file.path else ""
                ) + str(
                    f"\ndeps: \n{pformat(asset_file.dependencies)}\n" if asset_file.dependencies else ""
                )
            )
            # Dependency Resolution
            dependencies: list[Engine.assets.LoadedAsset] = self._dependency_resolver.resolve(asset_file)

            # We get the corresponding branch
            branch: AssetRoster = self.get_branch(asset_file.type.name)

            # Uploading content
            content: Any = branch.loader.load(asset_file)

            # Creating an asset object_node
            dependencies.extend(loaded_dependencies)
            asset_data = branch.loader.create(
                asset_file=asset_file,
                dependencies=dependencies,
                content=content
            )

            # Saving to the appropriate branch
            with Engine.threading.Thread.global_lock:
                branch[asset_data.id] = asset_data

            logger.success(f"AssetManager - Asset {asset_file.id} loaded\n")
            return Engine.assets.LoadedAsset(
                branch_id=branch.id,  # The name of the parent branch of the type
                id=asset_data.id
            )

        except KeyError as e:
            raise InvalidAssetTypeError(f"Unregistered type: {asset_file.type.name}") from e
