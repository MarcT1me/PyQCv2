from typing import Optional, List, Dict
from dataclasses import dataclass, field

import Engine.data


@dataclass(kw_only=True)
class AppData(Engine.data.MetaData):
    """ App Data class """
    fps: int  # clock
    data_table: Optional[Engine.data.arrays.DataTable] = field(default_factory=Engine.data.arrays.DataTable)  # data

    """ Scene and space context """
    root_scene_id: Engine.data.Identifier = field(default=None)

    """ Error catching """
    failures: List[Engine.failures.Failure] = field(init=False, default_factory=list)

    """ Events """
    joysticks: Dict[int, Engine.pg.joystick.JoystickType] = field(init=False, default_factory=dict)
