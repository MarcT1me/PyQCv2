""" Error handling during engine operation
"""
from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any, Self, Optional
from loguru import logger

import Engine


@dataclass(kw_only=True)
class Failure(Exception, Engine.data.TimedMetaData):
    """ A common error class """
    catch_id: 'Engine.data.Identifier | None' = field(default=None)
    critical: bool = field(default=True)
    err: Exception | None = None

    def wrap(self, exc:  Exception):
        """ Wraps failure into given exception """
        raise exc from self.err


class FailuresRoster(Engine.data.arrays.SimpleRoster):
    def __contains__(self, item):
        for failure in self.values():
            if item == type(failure.err) or item == failure.err:
                return True
        return False


class IFailureHandler:
    @abstractmethod
    def on_failure(self, err: Failure):
        """ Handling failure from catching """


class Catch:
    """ A context manager for eliminating errors in their storage and processing,
    contains a method for unhindered launching of dangerous functions.
    """
    roster: Engine.data.arrays.SimpleRoster[str, Self] = Engine.data.arrays.SimpleRoster()

    def __init__(self, *,
                 identifier: Optional[Engine.data.IdentifierType] = None,
                 handler: IFailureHandler = None,
                 critical: bool = True, is_handling: bool = True) -> None:
        self.id = Engine.data.Identifier.from_uncertain(identifier) if identifier else Engine.data.Identifier()

        if identifier in Catch.roster:
            RuntimeError(f"Catch with the name {identifier} already in Catch.list")

        self.failures: FailuresRoster[str, Failure] = FailuresRoster()
        self.critical = critical
        self.is_handling = is_handling
        self.handler = handler

        Catch.roster[self.id] = self

    def try_func(self, func: Engine.FUNC, *args, **kwargs) -> Any:
        try:
            func(*args, **kwargs)
        except Exception as exc:
            exc._is_try_func = True
            self.__got_error(type(exc), exc, False)

    def __enter__(self) -> Self:
        return self

    def handle_err(self, err: Failure):
        if self.is_handling:
            if self.handler:
                (self.handler if self.handler is not None else Engine.App.instance).on_failure(err)

    def __got_error(self, exc_type: type, exc_val: Exception | Failure, critical: bool):
        # Проверяем, является ли исключение экземпляром класса Exception или его подкласса
        logger.warning(f"Catch {self.id} got a {'critical' if critical else 'not critical'} error {exc_type}")
        if issubclass(exc_type, Failure):
            exc_val.catch_id = self.id
            err = exc_val
            self.handle_err(err)
        else:
            err: Failure = Failure(catch_id=self.id, critical=critical, err=exc_val)
            self.handle_err(err)
        self.failures[err.id] = err

    def __exit__(self, exc_type: type, exc_val: Failure | Exception, _) -> True:
        if exc_type is not None:
            self.__got_error(exc_type, exc_val, self.critical)
        Catch.roster.pop(self.id)
        return True
