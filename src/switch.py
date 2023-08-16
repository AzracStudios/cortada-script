from typing import Any, Callable, TypeAlias, TypeVar

T = TypeVar("T")


class ReturnableCase:
    def __init__(self, case: Any, do: Any):
        self.case: Any = case
        self.do: Any = do

    def eval(self, variable: Any) -> Any | None:
        if variable in self.case:
            return self.do


class AuxiliaryCase:
    def __init__(self, case: Any, do: Any, variable: Any):
        self.case: Any = case
        self.variable: Any = variable
        self.do: Any = do

    def eval(self, variable: Any) -> Any | None:
        if self.variable in self.case:
            return self.do


class ExecutableCase:
    def __init__(self, case: Any, do: Callable):
        self.case: Any = case
        self.do: Callable = do

    def eval(self, variable: Any) -> Any | None:
        if variable in self.case:
            return self.do(variable)


Case: TypeAlias = ReturnableCase | ExecutableCase | AuxiliaryCase


class Switch:
    def __init__(self, variable: T, cases: list[Case]) -> None:
        self.variable: T = variable
        self.cases: list[Case] = cases

    def eval(self) -> T | None:
        for case in self.cases:
            if res := case.eval(self.variable):
                return res
