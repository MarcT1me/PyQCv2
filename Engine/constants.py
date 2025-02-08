""" Engine CONSTANTS
"""
from enum import Flag, auto
from typing import TypeVar, Callable, Any

""" types """
T = TypeVar('T', bound=object)
FUNC = TypeVar('FUNC', bound=Callable[..., Any])
CLS = TypeVar('CLS', bound=type)


# Engine default values
class DataType(Flag):
    BINARY = auto()
    TEXT = auto()
    CONFIG = auto()
    ASSET = auto()
    NETWORK = auto()


class ResultType(Flag):
    SUCCESS = auto()
    NOT_FINISHED = auto()


# flags
class ShaderType(Flag):
    """ GLSL shader file types """
    VERTEX_SHADER = auto()
    FRAGMENT_SHADER = auto()
    GEOMETRY_SHADER = auto()
    COMPUTE_SHADER = auto()
