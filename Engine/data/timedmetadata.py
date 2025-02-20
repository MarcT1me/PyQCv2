from dataclasses import dataclass, field
from time import time

from Engine.data.metadata import MetaData


@dataclass(kw_only=True)
class TimedMetaData(MetaData):
    time_stamp: float = field(default_factory=time)
