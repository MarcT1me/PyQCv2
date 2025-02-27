from typing import Optional
from dataclasses import dataclass, InitVar, field

import Engine.data


@dataclass(kw_only=True)
class AppData(Engine.data.MetaData):
    fps: int  # clock
    data_table: Engine.data.arrays.DataTable  # data
    assets_type_configs: list[Engine.assets.AssetLoader]  # assets

    # other
    running: bool = field(init=False, default=True)
    win_data: Engine.graphic.WinData = field(init=False)
    gl_data: Optional[Engine.graphic.GL.GlData] = field(init=False, default=None)
