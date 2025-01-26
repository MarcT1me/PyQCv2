from dataclasses import dataclass, field

from Engine.objects.metadata import MetaData


@dataclass(init=True)
class AssetData(MetaData):
    asset_type: str | None = None
    dependencies: list[str] = field(default_factory=list)
