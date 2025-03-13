""" Engine threads controlling """
from typing import Self, Optional, final
from threading import Thread as _PyThread
from threading import Lock, Condition, current_thread

import Engine


class ThreadError(Exception): pass


class AlreadyExistThreadError(ThreadError): pass


class PendingThreadNotExistError(ThreadError): pass


class ThreadReleaseError(ThreadError): pass


class ThreadWarning(Warning): pass


class ThreadActionWarning(ThreadWarning): pass


class ThreadJoinWarning(ThreadWarning): pass


class ThreadRoster(Engine.data.arrays.SimpleRoster):
    pending: Engine.data.arrays.SimpleRoster[str, 'Thread']
    worked: Engine.data.arrays.SimpleRoster[str, 'Thread']


class Thread(_PyThread):
    _roster: ThreadRoster[str, Self] = ThreadRoster()

    @staticmethod
    def create_lock() -> Lock:
        return Lock()

    global_lock = create_lock()

    @staticmethod
    def create_condition() -> Condition:
        return Condition()

    important = create_condition()
    important_id: Optional[str] = None

    is_critical_failures: bool = True

    def __init__(
            self,
            name: Optional[str] = None,
            *,
            action: Optional[Engine.FUNC] = None,
            daemon: bool = True,
            is_critical_failures: Optional[bool] = None
    ) -> Self:
        identifier = Engine.data.Identifier(name=name)

        if identifier in self._roster.pending:
            raise AlreadyExistThreadError(f"Thread with id: {identifier} already exist")

        super().__init__(name=identifier.name, daemon=daemon)
        self.id = identifier

        self._action_result = Engine.ResultType.NOT
        self.action = action or self.action

        self.is_critical_failures = is_critical_failures if is_critical_failures is not None else \
            Thread.is_critical_failures

        with Thread.global_lock:
            self._roster.pending[identifier] = self

    def action(self):
        """Base action method to be overridden"""
        raise NotImplementedError("Thread action must be implemented")

    @final
    def run(self):
        with Thread.important:
            while Thread.important_id is not None and Thread.important_id is not self.id:
                Thread.important.wait()

            with Thread.global_lock:
                try:
                    self._roster.worked[self.id] = self._roster.pending.pop(self.id)
                except KeyError as e:
                    raise PendingThreadNotExistError(
                        f"There is no waiting thread with id {self.id} in Thread.roster.pending"
                    ) from e

            with Engine.failures.Catch(is_critical=self.is_critical_failures, handler=self):
                self._action_result = self.action()

        self.release()

    @property
    @final
    def result(self):
        """Get thread execution result"""
        return Engine.data.ReturnValue(self._action_result, Engine.ResultType.Finished)

    def release(self):
        """Cleanup resources across all roster branches"""
        with self.global_lock:
            try:
                for branch in self._roster.branches:
                    if self.id in branch:
                        del branch[self.id]
            except KeyError as e:
                raise ThreadReleaseError(f"Cant release thread with id: {self.id}") from e

    def join(self, timeout: Optional[float] = None):
        try:
            super().join(timeout)
        except RuntimeError as e:
            raise ThreadJoinWarning(f"Cant join thread with id: {self.id}") from e
        finally:
            self.release()

    @classmethod
    def wait_pending(cls):
        while cls._roster.pending:
            Engine.timing.TimingSystem.wait(10)

    @classmethod
    def wait_worked(cls, timeout: Optional[float] = None, from_thread_id: Optional[str] = None):
        cls.join_roster(timeout, from_thread_id=from_thread_id)

    @classmethod
    def wait(cls):
        cls.wait_pending()
        cls.wait_worked()

    @final
    def set_important(self):
        try:
            Thread.important_id = self.id
            Thread.wait_worked(from_thread_id=self.id)
        except Exception as e:
            raise ThreadError(f"Cant set thread with id: {self.id} as important") from e

    @staticmethod
    @final
    def mute_important():
        Thread.important_id = None
        Thread.important.notify_all()

    @classmethod
    @final
    def current_thread_id(cls) -> Self:
        return current_thread().name

    @classmethod
    def join_roster(
            cls,
            timeout: Optional[float] = None,
            *,
            from_thread_id: Optional[str] = None
    ) -> None:
        filter_func = lambda x: x.id == from_thread_id if from_thread_id else True
        try:
            cls._roster.worked.use("join", filter_func, timeout)
            cls._roster.pending.use("join", filter_func, timeout)
        except RuntimeError as e:
            raise ThreadJoinWarning("Cant join thread roster") from e
