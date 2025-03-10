""" Error handling during engine operation
"""
from typing_extensions import deprecated
from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Self, Optional, final
from loguru import logger

import Engine


@dataclass(kw_only=True)
@final
class Failure(Exception, Engine.data.TimedMetaData):
    """ A common error class """
    catch_id: 'Engine.data.Identifier | None' = field(default=None)
    critical: bool = field(default=True)
    err: Exception | None = None

    @deprecated("This method makes it more difficult to read logs")
    def wrap(self, exc: Exception):
        """ Wraps failure into given exception """
        raise exc from self.err


@final
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


@final
class Catch:
    """ A context manager for eliminating errors in their storage and processing,
    contains a method for unhindered launching of dangerous functions.
    """
    roster: Engine.data.arrays.SimpleRoster[str, Self] = Engine.data.arrays.SimpleRoster()

    def __init__(self, *,
                 identifier: Optional[Engine.data.IdentifierType] = None,
                 handler: IFailureHandler = None,
                 is_critical: bool = True, is_handling: bool = True) -> None:
        self.id = Engine.data.Identifier.from_uncertain(identifier) if identifier else Engine.data.Identifier()

        if identifier in Catch.roster:
            RuntimeError(f"Catch with the name {identifier} already in Catch.list")

        self.failures: FailuresRoster[str, Failure] = FailuresRoster()
        self.critical = is_critical
        self.is_handling = is_handling
        self.handler = handler

        Catch.roster[self.id] = self

    def try_func(self, func: Engine.FUNC, *args, **kwargs) -> 'Any | Engine.ResultType.Error':
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            exc._is_try_func = True
            self._got_error(type(exc), exc, False)
            return Engine.ResultType.Error

    def __enter__(self) -> Self:
        return self

    def _handle_err(self, err: Failure):
        if self.is_handling:
            if self.handler:
                self.handler.on_failure(err)
            else:
                Engine.App.instance.on_failure(err)

    def _got_error(self, exc_type: type, exc_val: Exception | Failure, critical: bool):
        # Проверяем, является ли исключение экземпляром класса Exception или его подкласса
        logger.warning(
            f"Catch {self.id} got a {'critical' if critical else 'not critical'} error {exc_type}:\n{exc_val}\n"
        )
        if issubclass(exc_type, Failure):
            exc_val.catch_id = self.id
            err = exc_val
            self._handle_err(err)
        else:
            err: Failure = Failure(catch_id=self.id, critical=critical, err=exc_val)
            self._handle_err(err)
        self.failures[err.id] = err

    def __exit__(self, exc_type: type, exc_val: Failure | Exception, _) -> True:
        if exc_type is not None:
            self._got_error(exc_type, exc_val, self.critical)
        Catch.roster.pop(self.id)
        return True
