""" Engine threads controlling """
from threading import Thread as _PyThread
from threading import Lock, Condition, current_thread
import uuid
from typing import Self, Callable, Optional

import Engine


class Thread(_PyThread):
    create_roster = lambda: Engine.arrays.Roster().new_branch("pending").new_branch("worked")
    _roster: Engine.arrays.Roster[str, Self] = create_roster()
    global_lock = Lock()

    important = Condition()
    important_id: Optional[str] = None

    critical: bool = False

    def __init__(
            self,
            identifier: Optional[str] = None,
            *,
            action: Optional[Callable] = None,
            daemon: bool = True
    ) -> Self:
        identifier = identifier or str(uuid.uuid4())
        if identifier in self._roster.pending:
            raise ValueError(f"Thread ID {identifier} already exists")

        super().__init__(name=identifier, daemon=daemon)
        self.id = identifier
        self._action_result = Engine.NotFinished
        self.action = action or self.action

        with Thread.global_lock:
            self._roster.pending[identifier] = self

    def action(self):
        """Base action method to be overridden"""
        raise NotImplementedError("Thread action must be implemented")

    def run(self):
        with Thread.important:
            while Thread.important_id is not None and Thread.important_id is not self.id:
                Thread.important.wait()

            with Thread.global_lock:
                self._roster.worked[self.id] = self._roster.pending.pop(self.id)

            with Engine.failures.Catch(critical=self.critical):
                self._action_result = self.action()

        self.release()

    @property
    def result(self):
        """Get thread execution result"""
        return self._action_result

    def release(self):
        """Cleanup resources across all roster branches"""
        with self.global_lock:
            for branch in self._roster.values():
                if self.id in branch:
                    del branch[self.id]

    def join(self, timeout: float = None):
        try:
            super().join(timeout)
        finally:
            self.release()

    @classmethod
    def wait_pending(cls):
        while cls._roster.pending:
            Engine.timing.wait(10)

    @classmethod
    def wait_worked(cls):
        while len(cls._roster.worked) > 1:
            Engine.timing.wait(10)

    @classmethod
    def wait(cls):
        cls.wait_pending()
        cls.wait_worked()

    def set_important(self):
        Thread.important_id = self.id
        Thread.wait_worked()

    def mute_important(self):
        Thread.important_id = None
        Thread.important.notify_all()

    @classmethod
    def current_thread_id(cls) -> Self:
        return current_thread().name

    @classmethod
    def join_roster(
        cls,
        timeout: Optional[float] = None,
        *,
        from_thread_id: Optional[str] = None
    ) -> None:
        filter_func = lambda x: x.id == from_thread_id if from_thread_id else lambda x: True
        cls._roster.worked.use("join", timeout, calling_filter=filter_func)
        cls._roster.pending.use("join", timeout, calling_filter=filter_func)
