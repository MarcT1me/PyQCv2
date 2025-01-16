import threading
import uuid
from typing import Self, Callable, Optional
from Engine.arrays import Roster


class Thread(threading.Thread):
    roster: Roster[str, Self] = Roster()

    global_lock: Optional[threading.Lock] = None

    important_id: Optional[Self] = None
    important = threading.Event()
    important.clear()

    def __init__(self, identifier: str = uuid.uuid4(), *,
                 target: Callable = None, daemon: bool = True):
        assert identifier not in Thread.roster, f"identifier {identifier} already in Thread.roster"
        super().__init__(name=identifier, daemon=daemon)
        self.id = identifier
        self.target = target
        self.lock = threading.Lock()
        Thread.roster[identifier] = self

    def _action(self):
        if Thread.important.is_set() and Thread.important_id != self.id:
            Thread.important.wait()
        self.target()

    def run(self):
        with self.lock:
            if Thread.global_lock and Thread.global_lock != self.lock:
                with Thread.global_lock:
                    self._action()
            else:
                self._action()

    def release(self): ...

    def join(self, timeout: float = None):
        super().join(timeout)
        self.release()

    @classmethod
    def set_global_lock(cls):
        cls.global_lock = cls.roster[cls.current_thread_id()].lock

    @classmethod
    def mute_global_lock(cls):
        cls.global_lock = None

    @classmethod
    def set_important(cls):
        cls.important_id = cls.current_thread_id()
        cls.important.set()

    @classmethod
    def mute_important(cls):
        cls.important_id = None
        cls.important.clear()

    @classmethod
    def current_thread_id(cls) -> Self:
        return threading.current_thread().name

    @classmethod
    def clear_roster(cls):
        cls.roster.release()

    @classmethod
    def join_roster(cls, timeout: float = None, *, called_thread=None):
        cls.roster.use("join",
                       timeout,
                       calling_filter=lambda i: i.id == called_thread)
