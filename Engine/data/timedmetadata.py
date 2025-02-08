from dataclasses import dataclass, field
from Engine.timing.system import uix_time

from Engine.data.metadata import MetaData


@dataclass
class TimedMetaData(MetaData):
    time_stamp: float = field(default_factory=uix_time)
