from dataclasses import dataclass
from typing import Optional

import Engine
from Engine.assets.asset_data import AssetData
from Engine.math import vec3, vec4


@dataclass
class PBRProperties:
    metallic: float = 0
    roughness: float = 0.5
    mr_texture_id: Optional[str] = None
    transmission: float = 1
    ior: float = 1


@dataclass
class SubsurfaceProperties:
    color: vec3 = vec3(1)
    radius: float = 0
    thickness: float = 1


@dataclass
class EmissionProperties:
    color: Optional[vec3] = None
    texture_id: Optional[str] = None
    intensity: float = 1


@dataclass
class NormalMapProperties:
    texture_id: Optional[str] = None
    scale: float = 1


@dataclass(init=True)
class MaterialData(AssetData):
    asset_type = Engine.DataType.Material
    shader_id: str = "default"

    albedo_color: vec4 = vec4(1)
    albedo_texture_id: Optional[str] = None

    pbr: Optional[PBRProperties] = None
    emission: Optional[EmissionProperties] = None
    normal_map: Optional[NormalMapProperties] = None
    subsurface: Optional[SubsurfaceProperties] = None

    is_double_sided: bool = False
    cast_shadows: bool = False
