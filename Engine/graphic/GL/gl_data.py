from dataclasses import dataclass, field, InitVar
from typing import Self

import Engine
from Engine.graphic.interface import HardInterface


@dataclass(kw_only=True)
class GlData(Engine.data.MetaData):
    win_data: 'InitVar[Engine.graphic.WinData]' = None
    # core
    major_version: int = field(default=3)
    minor_version: int = field(default=3)
    profile_mask: int = field(default=Engine.pg.GL_CONTEXT_PROFILE_CORE)

    # window space
    view: Engine.math.vec4 = field(init=False)
    resolution: Engine.math.vec2 = field(init=False)
    # render distance
    near: float = field(default=0.01)
    far: float = field(default=300.0)

    # functions arguments
    clear_color: Engine.math.vec4 = field(default=Engine.math.vec4(0.08, 0.16, 0.18, 1.0))
    blend_func: tuple = field(default=(Engine.mgl.SRC_ALPHA, Engine.mgl.ONE_MINUS_SRC_ALPHA))
    flags: int = field(default=Engine.mgl.DEPTH_TEST | Engine.mgl.CULL_FACE | Engine.mgl.BLEND)

    # interface type
    interface_type: type = field(default=HardInterface)
    interface_resolution: Engine.math.vec2 = None

    def __post_init__(self, win_data: 'Engine.graphic.WinData'):
        self.view = Engine.math.vec4(0, 0, *win_data.size)
        self.resolution = Engine.math.vec2(win_data.size)
        self.interface_resolution = self.interface_resolution if self.interface_resolution else self.resolution

    def modify(self, changes: dict) -> Self:
        """ extern ths win_data and return new """
        [setattr(self, var, value) for var, value in changes.items()]
        return self
