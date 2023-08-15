from typing import Any, Callable, TypeAlias


class ReturnableCase:
    def __init__(self, case: Any, do: Any):
        self.case: Any = case
        self.do: Any = do

    def eval(self, variable: Any) -> Any | None:
        if variable in self.case:
            return self.do


class ExecutableCase:
    def __init__(self, case: Any, do: Callable):
        self.case: Any = case
        self.do: Callable = do

    def eval(self, variable: Any) -> Any | None:
        if variable in self.case:
            return self.do(variable)


Case: TypeAlias = ReturnableCase | ExecutableCase


class Switch:
    def __init__(self, variable: Any, cases: list[Case]) -> None:
        self.variable: Any = variable
        self.cases: list[Case] = cases
        

    def eval(self) -> Any | None:
        for case in self.cases:
            if res := case.eval(self.variable):
                return res
