from dataclasses import dataclass
from typing import Optional, List

import Engine
from Engine.assets.asset_data import AssetData
from Engine.assets.asset_loader import AssetLoader


@dataclass(kw_only=True)
class ShaderAssetData(AssetData):
    type = Engine.DataType.Shader
    content: 'Engine.graphic.GL.Shader'
    shader_type: Engine.ShaderType
    is_in_roster: bool = False


@dataclass(kw_only=True)
class GLSLShaderAssetData(AssetData):
    content: str


class GLSLShaderLoader(AssetLoader):
    def load(self, asset_file: 'Engine.assets.AssetFileData') -> str:
        return asset_file.path.open(
            mode="r" if asset_file.type.major | Engine.DataType.Text else "br"
        ).read()

    def create(self, asset_file: 'Engine.assets.AssetFileData',
               dependencies: 'Optional[List[Engine.assets.LoadedAsset]]', content: str) -> 'Engine.assets.AssetData':
        return GLSLShaderAssetData(
            type=asset_file.type,
            content=content
        )


class ShaderLoader(AssetLoader):
    def load(self, asset_file: 'Engine.assets.AssetFileData') -> None:
        pass

    def create(self, asset_file: 'Engine.assets.AssetFileData',
               dependencies: 'Optional[List[Engine.assets.LoadedAsset]]', content: None) -> 'Engine.assets.AssetData':
        content = {}
        shader_type = Engine.ShaderType(0)
        for dep in dependencies:
            dep_shader_type = dep.asset_data.type.minor
            content[dep_shader_type.name] = dep
            shader_type |= dep_shader_type

        return ShaderAssetData(
            id=asset_file.id,
            shader_type=shader_type,
            content=Engine.graphic.GL.Shader(
                Engine.graphic.GL.ShaderData(
                    id=asset_file.id,
                    shader_type=shader_type,
                    content=content
                )
            )
        )
