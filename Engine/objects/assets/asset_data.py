from dataclasses import dataclass, field
from typing import Optional

from Engine.objects.metadata import MetaData


@dataclass(init=True)
class AssetData(MetaData):
    asset_type: Optional[str] = None
    dependencies: list[str] = field(default_factory=list)
