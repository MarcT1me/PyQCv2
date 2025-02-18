from dataclasses import dataclass, field
from time import time

from Engine.data.metadata import MetaData


@dataclass
class TimedMetaData(MetaData):
    time_stamp: float = field(default_factory=time)
