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
    list: Dict[str, Self] = {}

    def __init__(self, _id=uuid4(), critical=True) -> None:
        self.id = uuid4()

        if _id in Catch.list:
            RuntimeError("Catch<id> arg already in Catch.list")

        self.failures: List[Failure] = []
        self.critical = critical

        Catch.list[_id] = self

    def try_func(self, func: Callable, *args, **kwargs) -> Any:
        try:
            func(*args, **kwargs)
        except Exception as exc:
            self.critical = False
            self.__exit__(type(exc), exc, None)

    @property
    def is_clear(self) -> bool:
        return bool(self.failures)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, _) -> True:
        if exc_type is not None:
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
        return True
