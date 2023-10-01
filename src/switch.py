class ReturnableCase:
    def __init__(self, case, do):
        self.case = case
        self.do = do

    def eval(self, variable):
        if variable in self.case:
            return self.do


class AuxiliaryCase:
    def __init__(self, case, do, variable):
        self.case = case
        self.variable = variable
        self.do = do

    def eval(self, variable):
        if self.variable in self.case:
            return self.do


class ExecutableCase:
    def __init__(self, case, do: Callable):
        self.case = case
        self.do: Callable = do

    def eval(self, variable):
        if variable in self.case:
            return self.do(variable)

class Switch:
    def __init__(self, variable, cases):
        self.variable = variable
        self.cases = cases

    def eval(self):
        for case in self.cases:
            if res := case.eval(self.variable):
                return res
