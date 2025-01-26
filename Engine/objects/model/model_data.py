from dataclasses import dataclass

from Engine.objects.assets.asset_data import AssetData


@dataclass(init=True)
class ModelData(AssetData):
    mesh_id: str = "default"
    model_type: str = "static"
