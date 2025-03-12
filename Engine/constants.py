""" Engine CONSTANTS
"""
from typing_extensions import (
    TypeVar as _TypeVar,
    Any as _Any,
    Type, Callable,
    Protocol,
    deprecated
)
from enum import Enum, Flag, auto

""" types """
T = _TypeVar('T', bound=object)
# simple types
FUNC = _TypeVar("FUNC", bound=Callable[..., _Any])
CLS = _TypeVar("CLS", bound=Type)
# args and kwargs
ARGS = _TypeVar("ARGS", bound=_Any)
KWARGS = _TypeVar("KWARGS", bound=_Any)


@deprecated("Used for typing, not for use.")
class Modifiable[T](Protocol):
    def modify(self: T, **changes: KWARGS) -> T:
        """
        Update multiple class attributes at once

        Args:
            changes: kwargs dictionary of new values - {item: new_value}

        Returns:
            current object after modifying

        Raises:
            AttributeError: if one of kwarg argument to change not in object
        """
        for item, value in changes.items():
            if hasattr(self, item):
                setattr(self, item, value)
            else:
                AttributeError("Cant set an undescribed attribute")
        return self


""" Enums and Flags """


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
