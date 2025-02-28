from typing import Optional, List, Dict
from dataclasses import dataclass, field

import Engine.data


@dataclass(kw_only=True)
class AppData(Engine.data.MetaData):
    """ App Data class """

    fps: int  # clock
    assets_type_configs: List[Engine.assets.AssetLoader]  # assets
    data_table: Optional[Engine.data.arrays.DataTable] = field(default_factory=Engine.data.arrays.DataTable)  # data

    """ Error catching """
    failures: List[Engine.failures.Failure] = field(init=False, default_factory=list)

    """ Events """
    joysticks: Dict[int, Engine.pg.joystick.JoystickType] = field(init=False, default_factory=dict)

    """ Scene and space context """
    root_scene_object_id: Engine.data.Identifier = field(init=False)

    win_data: Engine.graphic.WinData = field(init=False)
    gl_data: Optional[Engine.graphic.GL.GlData] = field(init=False, default=None)
