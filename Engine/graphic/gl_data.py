from dataclasses import dataclass, field
from typing import Self, Optional

from Engine.objects import MetaData
from Engine.math import vec4, vec2
from Engine.mgl import (DEPTH_TEST, CULL_FACE, BLEND,
                        SRC_ALPHA, ONE_MINUS_SRC_ALPHA)
from Engine.pg import GL_CONTEXT_PROFILE_CORE
from Engine.graphic.interface import HardInterface
from Engine.data import Win


@dataclass
class GlData(MetaData):
    # core
    major_version: int = field(default=3)
    minor_version: int = field(default=3)
    profile_mask: int = field(default=GL_CONTEXT_PROFILE_CORE)

    # window space
    view: vec4 = field(default_factory=lambda: vec4(0, 0, *Win.size))
    resolution: vec2 = field(default_factory=lambda: vec2(Win.size))
    # render distance
    near: float = field(default=0.01)
    far: float = field(default=300.0)

    # functions arguments
    clear_color: vec4 = field(default=vec4(0.08, 0.16, 0.18, 1.0))
    blend_func: tuple = field(default=(SRC_ALPHA, ONE_MINUS_SRC_ALPHA))
    flags: int = field(default=DEPTH_TEST | CULL_FACE | BLEND)

    # interface type
    interface_type: type = field(default=HardInterface)
    interface_resolution: Optional[vec2] = None

    def __post_init__(self):
        if self.interface_resolution is None:
            self.interface_resolution = self.resolution

    def extern(self, changes: dict) -> Self:
        """ extern ths win_data and return new """
        [setattr(self, var, value) for var, value in changes.items()]
        return self
