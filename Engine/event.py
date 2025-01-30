from abc import ABC

import Engine


class Event(ABC):
    __child: dict[str, type] = {}
    __event_counter = Engine.pg.USEREVENT + 1

    def __init_subclass__(cls, **kwargs):
        if Event.__event_counter >= Engine.pg.NUMEVENTS:
            raise RuntimeError("Exceeded maximum number of event types")

        if cls.__name__ not in Event.__child:
            cls._event_type = Event.__event_counter
            Event.__event_counter += 1
            Event.__child[cls.__name__] = cls
        super().__init_subclass__(**kwargs)

    def __init__(self):
        self._event: Engine.pg.event.Event = Engine.pg.event.Event(self.__class__._event_type)

    def update(self) -> None:
        self._event.__dict__.update(self._serialize_data())

    @property
    def event(self) -> Engine.pg.event.Event:
        return self._event

    def post(self):
        self.update()
        Engine.pg.event.post(self._event)

    def _serialize_data(self):
        return {
            k: v for k, v in self.__dict__.items()
            if not k.startswith("_")
        }

    @classmethod
    def _get_class(cls, type_name):
        if type_name not in Event.__child:
            raise ValueError(f"Unknown event type: {type_name}")
        return Event.__child[type_name]
