from dataclasses import dataclass, field
from Engine.objects import MetaDate
from Engine.math import vec2, vec4
from Engine.mgl import (DEPTH_TEST, CULL_FACE, BLEND,
                        SRC_ALPHA, ONE_MINUS_SRC_ALPHA)
from Engine.pg import GL_CONTEXT_PROFILE_CORE
from Engine.graphic.interface import HardInterface


@dataclass
class GlData(MetaDate):
    # core
    major_version: int = field(default=3)
    minor_version: int = field(default=3)
    profile_mask: int = field(default=GL_CONTEXT_PROFILE_CORE)
    view_start: vec2 = field(default=vec2(0))
    near: float = field(default=0.01)
    fara: float = field(default=300.0)
    clear_color: vec4 = field(default=vec4(0.08, 0.16, 0.18, 1.0))
    blend_func: tuple = field(default=(SRC_ALPHA, ONE_MINUS_SRC_ALPHA))
    interface_class: type = field(default=HardInterface)
    flags: int = field(default=DEPTH_TEST | CULL_FACE | BLEND)
