""" Engine time manager
"""
from typing import final
from loguru import logger
from time import time as uix_time

import Engine


@final
class SystemRoster(Engine.data.arrays.SimpleRoster):
    timers: Engine.data.arrays.AttributesKeeper[str, float] = Engine.data.arrays.AttributesKeeper(default=0)
    deferred_events: dict[str, Engine.pg.event.Event]


@final
class TimingSystem:
    """Engine time manager with deferred events and timers

    Attributes:
        delta (float): Time between last two ticks in seconds
        start (float): Timestamp of Clock initialization
        fps (float): Value of Frames Per Second
    """

    def __init__(self, fps: float = 0):
        self.start: float = uix_time()
        logger.info(
            f"Engine timing System - init data:\n"
            f"start: {self.start},\n"
            f"fps: {fps}"
        )
        self.__pg_clock = Engine.pg.time.Clock()
        self.delta: float = 0.0
        self.fps = fps

        # Initialize roster with dedicated branches
        self._roster: SystemRoster = SystemRoster(default=0)
        self.__event_counter = 0

        logger.success(
            f"Engine timing System - init\n"
        )

    def get_fps(self) -> float:
        """Get current FPS count"""
        return self.__pg_clock.get_fps()

    def get_time(self) -> int:
        """Get milliseconds since last tick"""
        return self.__pg_clock.get_time()

    @staticmethod
    def wait(ms: int) -> None:
        """Wait specified milliseconds"""
        Engine.pg.time.wait(ms)

    @staticmethod
    def get_ticks() -> int:
        """Get milliseconds since program start"""
        return Engine.pg.time.get_ticks()

    def tick(self) -> float:
        """Update clock and process deferred events"""
        self._process_deferred()
        return self.__pg_clock.tick(self.fps)

    def timer(self, name: str, cooldown: float) -> bool:
        """Check if timer is ready to trigger"""
        current_time = uix_time()
        last_time = self._roster.timers.get(name, 0)

        if current_time - last_time >= cooldown:
            self._roster.timers[name] = current_time
            return True
        return False

    def defer_event(self, event: Engine.pg.event.Event, delay: float) -> None:
        """Schedule event for deferred execution"""
        event_key = f"def_{self.__event_counter}"
        self.__event_counter += 1

        event.__dict__.update({
            "name": event_key,
            "used": False,
            "start": uix_time(),
            "delay": delay,
            "end": uix_time() + delay
        })

        self._roster.deferred_events[event_key] = event

    def cancel_deferred(self, event: Engine.pg.event.Event) -> None:
        """Cancel scheduled deferred event"""
        if event.name in self._roster.deferred_events:
            del self._roster.deferred_events[event.name]
        event.used = True

    def _process_deferred(self) -> None:
        """Process and trigger ready deferred events"""
        current_time = uix_time()
        to_remove = []

        for event_key, event in self._roster.deferred_events.items():
            if event.end <= current_time:
                event.used = True
                event.end = current_time
                Engine.pg.event.post(event)
                to_remove.append(event_key)

        for key in to_remove:
            del self._roster.deferred_events[key]
