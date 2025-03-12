""" Managing and creating shaders
"""
from typing import Any

import Engine
from Engine.graphic.GL.gl_object.gl_object import GlObject


class ShaderError(Exception): pass


class Shader(GlObject):
    data: 'Engine.graphic.GL.ShaderData'
    # ShaderData
    content: dict[Engine.assets.LoadedAsset]
    shader_type: Engine.ShaderType

    def __init__(self, data: 'Engine.graphic.GL.ShaderData'):
        super().__init__(data)
        try:
            """ selecting a type and creating a program """
            if self.data.shader_type == Engine.ShaderType.Compute:
                self.program: Engine.mgl.Program = Engine.App.graphic.__gl_system__.context.compute_shader(
                    self.data.content["Compute"].content
                )
            else:
                program_kwargs = {}
                if self.data.shader_type & Engine.ShaderType.Vertex and self.data.shader_type & Engine.ShaderType.Fragment:
                    program_kwargs['vertex_shader'] = self.data.content["Vertex"].content
                    program_kwargs['fragment_shader'] = self.data.content["Fragment"].content
                if self.data.shader_type & Engine.ShaderType.Geometry:
                    program_kwargs['geometry_shader'] = self.data.content["Geometry"].content
                # simple program creating
                self.program: Engine.mgl.Program = Engine.App.graphic.__gl_system__.context.program(**program_kwargs)
        except Exception as e:
            raise ShaderError(f"failed to init shader {self.id}") from e

    def __setitem__(self, u_name: str, u_value: Any):
        try:
            self.program[u_name] = u_value
        except KeyError as e:
            raise ShaderError(f'uniform `{u_name}` not used in shader') from e

    def __getitem__(self, u_name: Engine.data.Identifier):
        return self.program.get(u_name, None)

    def __release__(self):
        self.program.release()
