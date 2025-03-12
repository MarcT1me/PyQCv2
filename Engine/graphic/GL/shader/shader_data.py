from dataclasses import dataclass

import Engine
from Engine.graphic.GL.gl_object.gl_object_data import GlObjectData


@dataclass(kw_only=True)
class ShaderData(GlObjectData):
    shader_type: Engine.ShaderType
    content: dict[Engine.assets.LoadedAsset]