from dataclasses import dataclass

from Engine.data import MetaData


@dataclass(init=True)
class ModelData(MetaData):
    mesh_id: str = "default"
    model_type: str = "static"
