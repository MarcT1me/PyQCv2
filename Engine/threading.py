import threading
import uuid
from abc import abstractmethod
from typing import Self, Callable, Optional

from Engine.arrays import Roster


class Thread(threading.Thread):
    pending: Roster[str, Self] = Roster()
    worked: Roster[str, Self] = Roster()

    important = threading.Condition()
    important_id: Optional[str] = None

    def __init__(self, identifier: str = uuid.uuid4(), *,
                 action: Callable = None, daemon: bool = True):
        assert identifier not in Thread.pending, f"identifier {identifier} already in Thread.roster"
        super().__init__(name=identifier, daemon=daemon)
        self.id = identifier
        self.action = action if action else self.action
        Thread.pending[identifier] = self

    @abstractmethod
    def action(self):
        ...

    def run(self):
        with Thread.important:
            while Thread.important_id is not None and Thread.important_id is not self.id:
                Thread.important.wait()
            Thread.worked[self.id] = Thread.pending.pop(self.id)
            self.action()
            self.release()

    def release(self):
        Thread.worked.pop(self.id) if self.id in Thread.worked else Thread.pending.pop(self.id)

    def join(self, timeout: float = None):
        super().join(timeout)
        self.release()

    @classmethod
    def waiting_pending(cls):
        while len(tuple(cls.pending)) != 0: pass

    @classmethod
    def wait_worked(cls):
        while len(tuple(cls.worked)) > 1: pass

    @classmethod
    def set_important(cls):
        cls.important_id = cls.current_thread_id()
        cls.wait_worked()

    @classmethod
    def mute_important(cls):
        cls.important_id = None
        cls.important.notify_all()

    @classmethod
    def current_thread_id(cls) -> Self:
        return threading.current_thread().name

    @classmethod
    def join_roster(cls, timeout: float = None, *, from_thread_id=None):
        cls.pending.use("join",
                        timeout,
                        calling_filter=lambda i: i.id == from_thread_id)
