""" Error handling during engine operation
"""
from dataclasses import dataclass, field
from typing import Any, Self
from uuid import uuid4
from loguru import logger

import Engine


@dataclass
class Failure(Exception, Engine.data.MetaData):
    """ A common error class """
    catch_id: str | None = field(default=None)
    critical: bool = field(default=True)
    err: Exception | None = None
    time_stamp: float = field(default_factory=Engine.timing.uix_time)


class FailuresRoster(Engine.arrays.Roster):
    def __contains__(self, item):
        for failure in self.values():
            if item == type(failure.err) or item == failure.err:
                return True
        return False


class Catch:
    """ A context manager for eliminating errors in their storage and processing,
    contains a method for unhindered launching of dangerous functions.
    """
    roster: dict[str, Self] = {}

    def __init__(self, identifier=uuid4(), critical=True) -> None:
        self.id = identifier

        if identifier in Catch.roster:
            RuntimeError(f"Catch with the name {identifier} already in Catch.list")

        self.failures: FailuresRoster[str, Failure] = FailuresRoster()
        self.critical = critical

        Catch.roster[identifier] = self

    def try_func(self, func: Engine.FUNC, *args, **kwargs) -> Any:
        try:
            func(*args, **kwargs)
        except Exception as exc:
            exc._is_try_func = True
            self.__got_error(type(exc), exc, False)

    @property
    def is_clear(self) -> bool:
        return bool(self.failures)

    def __enter__(self) -> Self:
        return self

    def __got_error(self, exc_type: type, exc_val: Exception | Failure, critical: bool):
        # Проверяем, является ли исключение экземпляром класса Exception или его подкласса
        logger.warning(f"Catch {self.id} got a {'critical' if critical else 'not critical'} error {exc_type}")
        if issubclass(exc_type, Failure):
            exc_val.catch_id = self.id
            err = exc_val
            Engine.app.App.InheritedСlass.on_failure(err)
        else:
            err: Failure = Failure(catch_id=self.id, critical=critical, err=exc_val)
            Engine.app.App.InheritedСlass.on_failure(err)
        self.failures[err.id] = err

    def __exit__(self, exc_type: type, exc_val: Failure | Exception, _) -> True:
        if exc_type is not None:
            self.__got_error(exc_type, exc_val, self.critical)
        Catch.roster.pop(self.id)
        return True
