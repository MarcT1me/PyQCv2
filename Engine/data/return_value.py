from typing import Any, final
from dataclasses import dataclass, InitVar, field

import Engine


@dataclass
@final
class ReturnValue:
    _value: Any
    best_result_type: InitVar[Engine.ResultType]
    result_type: Engine.ResultType = field(init=False)

    def __post_init__(self, best_result_type: Engine.ResultType):
        self.result_type = best_result_type if self._value is not Engine.ResultType.NOT else Engine.ResultType(
            best_result_type.value + Engine.ResultType.NOT.value
        )

    @property
    def result(self) -> Any:
        return self._value
