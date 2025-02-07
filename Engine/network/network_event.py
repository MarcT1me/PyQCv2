from typing import Self
from abc import ABC

from Engine.events.event import Event


class NetworkEvent(Event, ABC):
    def to_dict(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "data": self._serialize_data()
        }

    @classmethod
    def from_dict(cls, event_dict) -> Self:
        event_class = cls._get_class(event_dict['type'])
        obj = event_class(**event_dict.get("data", {}))
        return obj
