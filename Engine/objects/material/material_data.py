from dataclasses import dataclass
from typing import Optional

from Engine.data import AssetData
from Engine.math import vec3


@dataclass
class PBRProperties:
    metallic: float = 0
    roughness: float = 0.5
    mr_texture_id: Optional[str] = None
    transmission: float = 1
    ior: float = 1


@dataclass
class SubsurfaceProperties:
    color: Optional[vec3] = vec3(1)
    radius: float = 0
    thickness: float = 1


@dataclass
class EmissionProperties:
    color: Optional[vec3] = vec3(1)
    texture_id: Optional[str] = None
    intensity: float = 1


@dataclass
class NormalMapProperties:
    texture_id: Optional[str] = None
    scale: float = 1


@dataclass(init=True)
class MaterialData(AssetData):
    shader_id: str = "default"

    albedo_color: vec3 = vec3(1)
    albedo_texture_id: Optional[str] = None
    alpha: float = 1

    pbr: Optional[PBRProperties] = None
    emission: Optional[EmissionProperties] = None
    normal_map: Optional[NormalMapProperties] = None
    subsurface: Optional[SubsurfaceProperties] = None

    is_double_sided: bool = False
    cast_shadows: bool = False
