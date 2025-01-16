from dataclasses import dataclass, field
from typing import Any, Self, Callable, Dict, List
from uuid import uuid4
import Engine


@dataclass
class Failure(Exception, Engine.objects.MetaDate):
    catch_id: str | None = field(default=None)
    critical: bool = field(default=True)
    err: Warning = field(default_factory=lambda: RuntimeError("Failure.err is Empty"))


class UnexpectedException(Exception):
    def __init__(self, exc_val):
        self.exc = exc_val
        super().__init__(f"Unexpected exception {exc_val}")


class Catch:
    roster: Dict[str, Self] = {}

    def __init__(self, identifier=uuid4(), critical=True) -> None:
        self.id = identifier

        if identifier in Catch.roster:
            RuntimeError("Catch<id> arg already in Catch.list")

        self.failures: List[Failure] = []
        self.critical = critical

        Catch.roster[identifier] = self

    def try_func(self, func: Callable, *args, **kwargs) -> Any:
        try:
            func(*args, **kwargs)
        except Exception as exc:
            self.critical = False
            self.__got_error(type(exc), exc)

    @property
    def is_clear(self) -> bool:
        return bool(self.failures)

    def __enter__(self) -> Self:
        return self

    def __got_error(self, exc_type, exc_val):
        # Проверяем, является ли исключение экземпляром класса Exception или его подкласса
        if issubclass(exc_type, Failure):
            exc_val.catch_id = self.id
            Engine.app.App.WorkAppType.on_failure(exc_val)
        elif issubclass(exc_type, Exception):
            err: Failure = Failure(catch_id=self.id, critical=self.critical, err=exc_val)
            Engine.app.App.WorkAppType.on_failure(err)
        else:
            err: Failure = Failure(catch_id=self.id, critical=self.critical, err=UnexpectedException(exc_val))
            Engine.app.App.WorkAppType.on_failure(err)

    def __exit__(self, exc_type, exc_val, exc_tb) -> True:
        if exc_type is not None:
            self.__got_error(exc_type, exc_val)
        Catch.roster.pop(self.id)
        return True
