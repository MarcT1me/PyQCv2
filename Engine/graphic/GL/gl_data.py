from dataclasses import dataclass, field, InitVar

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
    view: Engine.math.ivec4 = field(default=None)
    resolution: Engine.math.ivec2 = field(default=None)
    # render distance
    near: float = field(default=0.01)
    far: float = field(default=300.0)

    # functions arguments
    clear_color: Engine.math.vec4 = field(default=Engine.math.vec4(0.08, 0.16, 0.18, 1.0))
    blend_func: tuple = field(default=(Engine.mgl.SRC_ALPHA, Engine.mgl.ONE_MINUS_SRC_ALPHA))
    flags: int = field(default=Engine.mgl.DEPTH_TEST | Engine.mgl.CULL_FACE | Engine.mgl.BLEND)

    # interface type
    interface_type: type = field(default=HardInterface)
    interface_resolution: Engine.math.ivec2 = None

    def __post_init__(self, win_data: 'Engine.graphic.WinData'):
        self.resolution = Engine.math.ivec2(win_data.size)
        self.view = Engine.math.vec4(0, 0, *self.resolution)
        self.interface_resolution = self.interface_resolution if self.interface_resolution else self.resolution
