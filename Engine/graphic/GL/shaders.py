""" Managing and creating shaders
"""
import moderngl
from loguru import logger

from Engine.constants import (
    ShaderType,
)
from Engine.data.config import File
import Engine.graphic


class Shader:
    def __init__(self, _path, shader_type, file_type=Engine.DataType.Text):
        """ Shader """
        self.id = None  # him id
        """ selecting a type and creating a program """
        if shader_type & ShaderType.Compute:
            self.program: moderngl.Program = Engine.app.App.graphic.context.compute_shader(
                self.__read_file__(_path + '.glsl', file_type)
            )
        else:
            program_kwargs = {}
            if shader_type & ShaderType.Vertex and shader_type & ShaderType.Fragment:
                program_kwargs['vertex_shader'] = self.__read_file__(_path + '.vert', file_type)
                program_kwargs['fragment_shader'] = self.__read_file__(_path + '.frag', file_type)
            if shader_type & ShaderType.Geometry:
                program_kwargs['geometry_shader'] = self.__read_file__(_path + '.glsl', file_type)
            # simple program creating
            self.program: moderngl.Program = Engine.app.App.graphic.context.program(**program_kwargs)

    @staticmethod
    def __read_file__(path: str, _type) -> str:
        """ read shader from file with path """
        if _type is Engine.DataType.Text:
            return Shader.__read_text_file__(path)
        elif _type is Engine.DataType.Binary:
            return Shader.__read_binary_file__(path)
        else:
            raise TypeError(f'cen\'t load shader from {_type} file type')

    @staticmethod
    def __read_text_file__(path: str):
        with open(path) as f:
            shader_source = f.read()
        return shader_source

    @staticmethod
    def __read_binary_file__(path: str):
        from dill import load
        with open(path + '.dill', 'br') as bf:
            shader_source = load(bf)
        return shader_source

    def __setitem__(self, u_name, u_value):
        try:
            self.program[u_name] = u_value
        except KeyError:
            logger.error(f'uniform `{u_name}` not used in shader')

    def __getitem__(self, u_name):
        return self.program.get(u_name, None)

    def __release__(self):
        self.program.release()
        if self.id is not None:
            ShadersProgram.roster.pop(self.id)


class ShadersProgram:
    roster: dict[str, Shader] = {}

    def __new__(cls, *args, **kwargs):
        if len(cls.roster) == 0:
            cls.roster['default-main'] = Shader(
                rf'{File.__ENGINE_DATA__}\shaders\default\main',
                ShaderType.Vertex | ShaderType.Fragment
            )

    @classmethod
    def __getitem__(cls, item):
        return cls.roster[item]

    @classmethod
    def add(cls, key: str, value: Shader):
        cls.roster[key] = value
        value.id = key

    @classmethod
    def __release__(cls):
        for shader in cls.roster.values():
            shader.__release__()

    @classmethod
    def clear(cls):
        cls.__release__()
        cls.roster.clear()
