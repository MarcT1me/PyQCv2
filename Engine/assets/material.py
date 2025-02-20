from dataclasses import dataclass
from typing import Optional

import Engine
from Engine.assets.asset_data import AssetData


@dataclass(kw_only=True)
class PBRProperties:
    metallic: float = 0
    roughness: float = 0.5
    mr_texture_id: Optional[Engine.data.Identifier] = None
    transmission: float = 1
    ior: float = 1


@dataclass(kw_only=True)
class SubsurfaceProperties:
    color: Engine.math.vec3 = Engine.math.vec3(1)
    radius: float = 0
    thickness: float = 1


@dataclass(kw_only=True)
class EmissionProperties:
    color: Optional[Engine.math.vec3] = None
    texture_id: Optional[Engine.data.Identifier] = None
    intensity: float = 1


@dataclass(kw_only=True)
class NormalMapProperties:
    texture_id: Optional[Engine.data.Identifier] = None
    scale: float = 1


@dataclass(kw_only=True)
class MaterialData(AssetData):
    type = Engine.DataType.Material
    shader_id: Engine.data.Identifier = "default"

    albedo_color: Engine.math.vec4 = Engine.math.vec4(1)
    albedo_texture_id: Optional[Engine.data.Identifier] = None

    pbr: Optional[PBRProperties] = None
    emission: Optional[EmissionProperties] = None
    normal_map: Optional[NormalMapProperties] = None
    subsurface: Optional[SubsurfaceProperties] = None

    is_double_sided: bool = False
    cast_shadows: bool = False
