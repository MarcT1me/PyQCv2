from typing import Dict, Set, List, Any, Self

import Engine


class AssetError(Exception):
    """Base class for all asset loading exceptions"""


class AssetRoster(Engine.data.arrays.SimpleRoster):
    def __init__(self, name: str, loader: 'Engine.assets.Loader | None', *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.loader = loader

    def definite(self, name) -> 'Engine.assets.AssetData':
        for asset in self.values():
            if asset.name == name:
                return asset
        raise AssetError(f"Cant find definite asset with name {name}")

    def new_branch(self, name: str, value: Any = dict(), *args, **kwargs) -> Self:
        super().new_branch(name, AssetRoster(name, *args, **kwargs))


class CyclicDependencyError(AssetError):
    pass


class MissingDependencyError(AssetError):
    pass


class DependencyResolver:
    def __init__(self, loading_func: Engine.FUNC):
        self.loading_func = loading_func
        self._loading_stack: Set[str] = set()
        self._dependency_cache: Dict[str, List[Engine.assets.LoadedAsset]] = {}

    def resolve(self, asset_file: 'Engine.assets.AssetFileData') -> 'List[Engine.assets.LoadedAsset]':
        """
        Retrieves the list of downloaded dependencies for the specified cassette
        with loop handling and caching
        """
        if asset_file.dependencies is None:
            return None

        cache_key = str(asset_file.path)

        # Returning cached dependencies
        if cache_key in self._dependency_cache:
            return self._dependency_cache[cache_key]

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
            self._dependency_cache[cache_key] = dependencies
            return dependencies
        except Exception as e:
            raise AssetError(f"Failed to load asset {asset_file}") from e
        finally:
            with Engine.threading.Thread.global_lock:
                self._loading_stack.remove(cache_key)

    def clear_cache(self):
        """ Clears the dependency cache """
        self._dependency_cache.clear()
        self._loading_stack.clear()


class InvalidAssetTypeError(AssetError):
    pass


class DuplicatedAssetTypeConfig(AssetError):
    pass


class AssetManager:
    def __init__(self, asset_loaders: 'list[Engine.assets.AssetLoader]'):
        # Initializing the root Roster
        self.storage: AssetRoster[str, AssetRoster[str, Engine.assets.AssetData]] = AssetRoster(name="root", loader=None)
        self.dependency_resolver = DependencyResolver(self.load)

        # Registering asset types as branches in the Roster
        self._register_asset_type(asset_loaders)

    def _register_asset_type(self, asset_loaders: 'list[Engine.assets.AssetLoader]'):
        asset_types: Dict[str, Engine.assets.AssetLoader] = {}

        for loader in asset_loaders:
            name = loader.type.get_name()
            if not loader:
                raise InvalidAssetTypeError("Loader not configured")
            elif name in asset_types:
                raise DuplicatedAssetTypeConfig(f"Asset type '{name}' already registered")

            # Creating a new branch in the Roster
            self.storage.new_branch(
                name=name,
                loader=loader
            )

            # Saving the config for quick access
            asset_types[name] = loader

    def get_branch(self, branch_name: str) -> AssetRoster:
        # We are looking for a branch by type name in the root Roster
        branch = self.storage.branch(branch_name)
        if branch is not None:
            return branch
        raise InvalidAssetTypeError(f"No branch with name {branch_name}")

    def load(self, asset_file: 'Engine.assets.AssetFileData') -> 'Engine.assets.LoadedAsset':
        try:
            # Dependency Resolution
            dependencies: List[Engine.assets.LoadedAsset] = self.dependency_resolver.resolve(asset_file)

            # We get the corresponding branch
            branch: AssetRoster = self.get_branch(asset_file.type.get_name())

            # Uploading content
            content: Any = branch.loader.load(asset_file)

            # Creating an asset object_node
            asset_data = branch.loader.create(
                asset_file=asset_file,
                dependencies=dependencies,
                content=content
            )

            # Saving to the appropriate branch
            with Engine.threading.Thread.global_lock:
                branch[asset_data.id] = asset_data

            return Engine.assets.LoadedAsset(
                branch_name=branch.name,  # The name of the parent branch of the type
                id=asset_data.id
            )

        except KeyError as e:
            raise InvalidAssetTypeError(f"Unregistered type: {asset_file.type}") from e
