""" Managing and creating shaders
"""
from typing import Any
import moderngl

import Engine
from Engine.graphic.GL.gl_object.gl_object import GlObject


class ShaderError(Exception): pass


class Shader(GlObject):
    data: 'Engine.graphic.GL.ShaderData'
    # ShaderData
    content: dict[Engine.assets.LoadedAsset]
    shader_type: Engine.ShaderType
    is_in_roster: bool

    def __init__(self, data: 'Engine.graphic.GL.ShaderData'):
        super().__init__(data)
        try:
            """ selecting a type and creating a program """
            if self.shader_type == Engine.ShaderType.Compute:
                self.program: moderngl.Program = Engine.App.graphic.context.compute_shader(
                    self.content["Compute"].data
                )
            else:
                program_kwargs = {}
                if self.shader_type & Engine.ShaderType.Vertex and self.shader_type & Engine.ShaderType.Fragment:
                    program_kwargs['vertex_shader'] = self.content["Vertex"].data
                    program_kwargs['fragment_shader'] = self.content["Fragment"].data
                if self.shader_type & Engine.ShaderType.Geometry:
                    program_kwargs['geometry_shader'] = self.content["Geometry"].data
                # simple program creating
                self.program: moderngl.Program = Engine.App.graphic.context.program(**program_kwargs)
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
        if self.id is not None:
            if self.is_in_roster:
                Engine.App.graphic.shader_roster.remove(self.id)
