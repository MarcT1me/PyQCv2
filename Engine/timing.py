""" Engine time manager
"""
from pygame.time import Clock as _pg_Clock
from pygame.time import get_ticks
from pygame.time import wait
from numpy import uint8
# standard
from time import time as uix_time
# Engine
import Engine


class System:
    """Engine time manager with deferred events and timers

    Attributes:
        delta (float): Time between last two ticks in seconds
        start (float): Timestamp of Clock initialization
    """

    def __init__(self):
        self.__pg_clock = _pg_Clock()
        self.start: float = uix_time()
        self.delta: float = 0.0

        # Initialize roster with dedicated branches
        self.roster = Engine.arrays.Roster(default=0)
        self.roster.new_branch("timers")
        self.roster.new_branch("deferred_events")
        self.__event_counter = uint8(0)

    def get_fps(self) -> float:
        """Get current FPS count"""
        return self.__pg_clock.get_fps()

    def get_time(self) -> int:
        """Get milliseconds since last tick"""
        return self.__pg_clock.get_time()

    @staticmethod
    def wait(ms: int) -> None:
        """Wait specified milliseconds"""
        wait(ms)

    @staticmethod
    def get_ticks() -> int:
        """Get milliseconds since program start"""
        return get_ticks()

    def tick(self, fps: float = 0) -> float:
        """Update clock and process deferred events"""
        self._process_deferred()
        return self.__pg_clock.tick(fps)

    def timer(self, name: str, cooldown: float) -> bool:
        """Check if timer is ready to trigger"""
        current_time = uix_time()
        last_time = self.roster.timers[name]

        if current_time - last_time >= cooldown:
            self.roster.timers[name] = current_time
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

        self.roster.deferred_events[event_key] = event

    def cancel_deferred(self, event: Engine.pg.event.Event) -> None:
        """Cancel scheduled deferred event"""
        if event.name in self.roster.deferred_events:
            del self.roster.deferred_events[event.name]
        event.used = True

    def _process_deferred(self) -> None:
        """Process and trigger ready deferred events"""
        current_time = uix_time()
        to_remove = []

        for event_key, event in self.roster.deferred_events.items():
            if event.end <= current_time:
                event.used = True
                event.end = current_time
                Engine.pg.event.post(event)
                to_remove.append(event_key)

        for key in to_remove:
            del self.roster.deferred_events[key]
