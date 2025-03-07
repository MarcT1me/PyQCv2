""" Engine CONSTANTS
"""
from enum import Enum, Flag, auto
from typing import TypeVar, Type, Callable, Any, Self

""" types """
T = TypeVar('T', bound=object)
FUNC = TypeVar('FUNC', bound=Callable[[...], Any])
CLS = TypeVar('CLS', bound=Type)
ARGS = TypeVar("ARGS", bound=Any)
KWARGS = TypeVar("KWARGS", bound=Any)


class DataType(Flag):
    Empty = auto()
    # file types
    File = auto()

    Text = auto()
    Toml = auto()
    Json = auto()

    Bin = auto()
    Dill = auto()
    Pickle = auto()

    PyGame = auto()
    # d vars
    D1 = auto()
    D2 = auto()
    D3 = auto()
    D4 = auto()

    UI = auto()
    # general
    Failure = auto()
    Catch = auto()
    Thread = auto()
    Joystick = auto()
    Asset = auto()
    Config = auto()
    Sav = auto()
    # animation
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

    UserDataType = auto()


class ResultType(Enum):
    Found = auto()
    NotFound = auto()

    Finished = auto()
    NotFinished = auto()

    Success = auto()
    Error = auto()

    NOT = 1


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
