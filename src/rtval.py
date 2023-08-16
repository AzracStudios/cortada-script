from position import *
from typing import Self
from error import *
from context import Context


class Value:
    def set_pos(
        self, start_pos: Position | None = None, end_pos: Position | None = None
    ) -> Self:
        self.start_pos = start_pos
        self.end_pos = end_pos
        return self

    def set_context(self, context: Context | None = None):
        self.context = context
        return self

    def added_to(self, other: Self) -> Self | None:
        raise Exception("Method not implemented")

    def subtracted_by(self, other: Self) -> Self | None:
        raise Exception("Method not implemented")

    def multiplied_by(self, other: Self) -> Self | None:
        raise Exception("Method not implemented")

    def divided_by(self, other: Self) -> Self | None:
        raise Exception("Method not implemented")

    def raised_to(self, other: Self) -> Self | None:
        raise Exception("Method not implemented")

    def comp_eq(self, other: Self) -> Self | None:
        raise Exception("Method not implemented")

    def comp_neq(self, other: Self) -> Self | None:
        raise Exception("Method not implemented")

    def comp_lt(self, other: Self) -> Self | None:
        raise Exception("Method not implemented")

    def comp_gt(self, other: Self) -> Self | None:
        raise Exception("Method not implemented")

    def comp_lte(self, other: Self) -> Self | None:
        raise Exception("Method not implemented")

    def comp_gte(self, other: Self) -> Self | None:
        raise Exception("Method not implemented")

    def comp_and(self, other: Self) -> Self | None:
        raise Exception("Method not implemented")

    def comp_or(self, other: Self) -> Self | None:
        raise Exception("Method not implemented")

    def unary_not(self) -> tuple[Self | None, Error | None]:
        raise Exception("Method not implemented")


class Number(Value):
    def __init__(self, value: int | float):
        self.value = value
        self.set_pos()
        self.set_context()

    # TODO: RETURN INVALID OPERAND FOR TYPES ERROR INSTEAD OF (None, None)
    def added_to(self, other: Value) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

        return None, None

    def subtracted_by(self, other: Value) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

        return None, None

    def multiplied_by(self, other: Value) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

        return None, None

    def divided_by(self, other: Value) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            if other.value == 0:
                return Number(float("inf")), None
            return Number(self.value / other.value).set_context(self.context), None

        return None, None

    def raised_to(self, other: Value) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            return Number(self.value**other.value).set_context(self.context), None

        return None, None

    def comp_eq(self, other: Self) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            return Boolean(self.value == other.value).set_context(self.context), None

        return None, None

    def comp_neq(self, other: Self) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            return Boolean(self.value != other.value).set_context(self.context), None

        return None, None

    def comp_lt(self, other: Self) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            return Boolean(self.value < other.value).set_context(self.context), None

        return None, None

    def comp_gt(self, other: Self) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            return Boolean(self.value > other.value).set_context(self.context), None

        return None, None

    def comp_lte(self, other: Self) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            return Boolean(self.value <= other.value).set_context(self.context), None

        return None, None

    def comp_gte(self, other: Self) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            return Boolean(self.value >= other.value).set_context(self.context), None

        return None, None

    def comp_and(self, other: Self) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            if type(self).__name__ == "Boolean":
                return (
                    Boolean(bool(self.value and other.value)).set_context(self.context),
                    None,
                )
            return Number(self.value and other.value).set_context(self.context), None

        return None, None

    def comp_or(self, other: Self) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            if type(self).__name__ == "Boolean":
                return (
                    Boolean(bool(self.value or other.value)).set_context(self.context),
                    None,
                )
            return Number(self.value or other.value).set_context(self.context), None

        return None, None

    def unary_not(self) -> tuple[Self | None, Error | None]:
        return Boolean(not self.value).set_context(self.context), None

    def copy(self) -> Self:
        copy = Number(self.value)
        copy.set_pos(self.start_pos, self.end_pos)
        copy.set_context(self.context)
        return copy

    def __repr__(self) -> str:
        return f"{self.value}"


class Boolean(Number):
    def __init__(self, value: bool):
        Number.__init__(self, int(value))

    def __repr__(self) -> str:
        return "true" if self.value else "false"
