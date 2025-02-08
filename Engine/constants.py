""" Engine CONSTANTS
"""
from enum import Flag, auto
from typing import TypeVar, Callable, Any

""" types """
T = TypeVar('T', bound=object)
FUNC = TypeVar('FUNC', bound=Callable[..., Any])
CLS = TypeVar('CLS', bound=type)


class FileType(Flag):
    Binary = auto()
    Dill = auto()
    Sav = auto()

    Text = auto()
    Config = auto()


class DataType(Flag):
    # space or var variable
    D1 = auto()
    D2 = auto()
    D3 = auto()
    # general
    Asset = auto()
    Failure = auto()
    Catch = auto()
    Thread = auto()
    Joystick = auto()
    Animation = auto()
    # audio
    AudioDevice = auto()
    AudioClip = auto()
    AudioChannel = auto()
    # video (future)
    VideoClip = auto()
    # graphics
    Window = auto()
    Renderer = auto()
    Shader = auto()
    Surface = auto()
    Texture = auto()
    # model
    Model = auto()
    Mesh = auto()
    Material = auto()
    # objects
    Object = auto()
    SceneObject = auto()
    RendererObject = auto()
    UiObject = auto()
    Camera = auto()
    Light = auto()


class ResultType(Flag):
    NotFinished = auto()
    Success = auto()
    Error = auto()


# flags
class ShaderType(Flag):
    """ GLSL shader file types """
    Vertex = auto()
    Fragment = auto()
    Geometry = auto()
    Compute = auto()

    # future (MirageAPI)
    Misl = auto()  # Mirage Shader Language. Example: interface.vert + interface.frag
    Mislib = auto()  # Mirage Shader Libreary. Example: pbr.mislib
    Micomp = auto()  # Mirage Compute (shader). Example: particle.micomp
