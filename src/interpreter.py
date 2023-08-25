from error import Error
from parser_nodes import *
from switch import *
from constants import *
from error import *
from rank import rank
from position import *
from typing import Self


class Context:
    def __init__(
        self,
        display_name: str,
        parent: Self | None = None,
        parent_entry_pos: Position | None = None,
    ) -> None:
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table: SymbolTable


class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def get(self, name):
        val = self.symbols.get(name, None)
        if not val and self.parent:
            return self.parent.get(name)
        return val

    def set(self, name, val):
        if val == None:
            val = Nil()
        self.symbols[name] = val

    def remove(self, name):
        del self.symbols[name]


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

    def get_value(self, context: Context | None = None):
        raise Exception("Method not implemented")

    def added_to(self, other: Self) -> tuple[Self | None, Error | None]:
        return (None, self.illegal_operation())

    def subtracted_by(self, other: Self) -> tuple[Self | None, Error | None]:
        return (None, self.illegal_operation())

    def multiplied_by(self, other: Self) -> tuple[Self | None, Error | None]:
        return (None, self.illegal_operation())

    def divided_by(self, other: Self) -> tuple[Self | None, Error | None]:
        return (None, self.illegal_operation())

    def raised_to(self, other: Self) -> tuple[Self | None, Error | None]:
        return (None, self.illegal_operation())

    def comp_eq(self, other: Self) -> tuple[Self | None, Error | None]:
        return (None, self.illegal_operation())

    def comp_neq(self, other: Self) -> tuple[Self | None, Error | None]:
        return (None, self.illegal_operation())

    def comp_lt(self, other: Self) -> tuple[Self | None, Error | None]:
        return (None, self.illegal_operation())

    def comp_gt(self, other: Self) -> tuple[Self | None, Error | None]:
        return (None, self.illegal_operation())

    def comp_lte(self, other: Self) -> tuple[Self | None, Error | None]:
        return (None, self.illegal_operation())

    def comp_gte(self, other: Self) -> tuple[Self | None, Error | None]:
        return (None, self.illegal_operation())

    def comp_and(self, other: Self) -> tuple[Self | None, Error | None]:
        return (None, self.illegal_operation())

    def comp_or(self, other: Self) -> tuple[Self | None, Error | None]:
        return (None, self.illegal_operation())

    def unary_not(self) -> tuple[Self | None, Error | None]:
        return (None, self.illegal_operation())

    def is_true(self) -> bool | Error:
        return self.illegal_operation()

    def copy(self):
        raise Exception("Copy Method Not Implemented")

    def execute(self, args) -> tuple[Self | None, Error | None]:
        return (
            None,
            TypeError(
                f"Cannot call {type(self)}",
                self.start_pos,  # type:ignore
                self.end_pos,  # type:ignore
                self.context,  # type:ignore
            ),
        )

    def illegal_operation(self, other=None):
        if not other:
            other = self
        return TypeError(
            f"Illegal operation for {type(self)} and {type(other)}",
            self.start_pos,  # type:ignore
            self.end_pos,  # type:ignore
            self.context,  # type:ignore
        )


class RTResult:
    def __init__(self):
        self.error: Error | None = None
        self.value: Value | None = None

    def register(self, res: Any) -> Value:
        if isinstance(res, RTResult):
            if res.error:
                self.error = res.error
            ##! I have no clue on how to fix the following line without breaking the rest of the code
            ##! If anyone reading this has any idea please submit a pr, thanks in advance :)
            return res.value  # type: ignore
        return res

    def success(self, value: Value) -> Self:
        self.value = value
        return self

    def failure(self, error: Error):
        self.error = error
        return self


class Number(Value):
    def __init__(self, value: int | float):
        self.value = value
        self.set_pos()
        self.set_context()

    def get_value(self, context: Context | None = None):
        return self.value

    def added_to(self, other: Value) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

        else:
            return None, self.illegal_operation(other)

    def subtracted_by(self, other: Value) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

        else:
            return None, self.illegal_operation(other)

    def multiplied_by(self, other: Value) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

        else:
            return None, self.illegal_operation(other)

    def divided_by(self, other: Value) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            if other.value == 0:
                return Number(float("inf")), None
            return Number(self.value / other.value).set_context(self.context), None

        else:
            return None, self.illegal_operation(other)

    def raised_to(self, other: Value) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            return Number(self.value**other.value).set_context(self.context), None

        else:
            return None, self.illegal_operation(other)

    def comp_eq(self, other: Self) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            return Boolean(self.value == other.value).set_context(self.context), None

        else:
            return None, self.illegal_operation(other)

    def comp_neq(self, other: Self) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            return Boolean(self.value != other.value).set_context(self.context), None

        else:
            return None, self.illegal_operation(other)

    def comp_lt(self, other: Self) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            return Boolean(self.value < other.value).set_context(self.context), None

        else:
            return None, self.illegal_operation(other)

    def comp_gt(self, other: Self) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            return Boolean(self.value > other.value).set_context(self.context), None

        else:
            return None, self.illegal_operation(other)

    def comp_lte(self, other: Self) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            return Boolean(self.value <= other.value).set_context(self.context), None

        else:
            return None, self.illegal_operation(other)

    def comp_gte(self, other: Self) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            return Boolean(self.value >= other.value).set_context(self.context), None

        else:
            return None, self.illegal_operation(other)

    def comp_and(self, other: Self) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            if type(self).__name__ == "Boolean":
                return (
                    Boolean(bool(self.value and other.value)).set_context(self.context),
                    None,
                )
            return Number(self.value and other.value).set_context(self.context), None

        else:
            return None, self.illegal_operation(other)

    def comp_or(self, other: Self) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            if type(self).__name__ == "Boolean":
                return (
                    Boolean(bool(self.value or other.value)).set_context(self.context),
                    None,
                )
            return Number(self.value or other.value).set_context(self.context), None

        else:
            return None, self.illegal_operation(other)

    def unary_not(self) -> tuple[Self | None, Error | None]:
        return Boolean(not self.value).set_context(self.context), None

    def copy(self) -> Self:
        copy = Number(self.value)
        copy.set_pos(self.start_pos, self.end_pos)
        copy.set_context(self.context)
        return copy

    def is_true(self) -> bool:
        return self.value != 0

    def __repr__(self) -> str:
        return f"{self.value}"


class Boolean(Number):
    def __init__(self, value: bool):
        Number.__init__(self, int(value))

    def copy(self) -> Self:
        copy = Boolean(bool(self.value))
        copy.set_pos(self.start_pos, self.end_pos)
        copy.set_context(self.context)
        return copy

    def __repr__(self) -> str:
        return "true" if self.value else "false"


class Nil(Number):
    def __init__(self):
        Number.__init__(self, 0)

    def copy(self) -> Self:
        copy = Nil()
        copy.set_pos(self.start_pos, self.end_pos)
        copy.set_context(self.context)
        return copy

    def __repr__(self) -> str:
        return "nil"


class String(Value):
    def __init__(self, value: str):
        self.value = value
        Value.__init__(self)

    def added_to(self, other: Self) -> tuple[Self | None, Error | None]:
        return String(self.value + f"{other.value}").set_context(self.context), None

    def multiplied_by(self, other: Number) -> tuple[Self | None, Error | None]:
        if isinstance(other, Number):
            return String(self.value * int(other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_value(self, context: Context | None = None):
        return self.value

    def is_true(self):
        return len(self.value) > 0

    def copy(self) -> Self:
        copy = String(self.value)
        copy.set_context(self.context)
        copy.set_pos(self.start_pos, self.end_pos)
        return copy

    def __repr__(self, inc_quotes: bool = True) -> str:
        return f'"{self.value}"' if inc_quotes else f"{self.value}"


class Function(Value):
    def __init__(self, name, body, args):
        self.name = name or "<anonymous>"
        self.body = body
        self.args = args

        Value.__init__(self)

    def copy(self) -> Self:
        copy = Function(self.name, self.body, self.args)
        copy.set_context(self.context)
        copy.set_pos(self.start_pos, self.end_pos)
        return copy

    def execute(self, args) -> RTResult:
        res = RTResult()
        new_context = Context(self.name, self.context, self.start_pos)
        new_context.symbol_table = SymbolTable(
            new_context.parent.symbol_table  # type:ignore
        )

        if len(args) != len(self.args):
            return res.failure(
                TypeError(
                    f"{self.name} takes in {len(self.args)} args. {args} {'args were' if args > 1 else 'arg was'} given",
                    self.start_pos,  # type:ignore
                    self.end_pos,  # type:ignore
                    self.context,  # type:ignore
                )
            )

        for i in range(len(args)):
            arg_name = self.args[i]
            arg_val = args[i]
            arg_val.set_context(new_context)
            new_context.symbol_table.set(arg_name, arg_val)

        val = res.register(Interpreter.visit(self.body, new_context))
        if res.error:
            return res

        return res.success(val)

    def __repr__(self):
        return f"<function {self.name}>"


#############################


def generate_hint(ctx, var_name):
    list_of_vars = []
    hint = None

    while ctx:
        list_of_vars.extend(ctx.symbol_table.symbols.keys())
        ctx = ctx.parent

    best_match = rank(list_of_vars, str(var_name), 3.14159)
    if len(best_match) > 0:
        best_match = best_match[0]
        if int(best_match["score"]) / len(str(var_name)) >= 0.3:
            hint = str(best_match["word"])

    if hint:
        hint = f"Did you mean {hint}?"

    return hint


class Interpreter:
    @staticmethod
    def visit(node: Node, context: Context) -> RTResult:
        method_name = f"visit_{type(node).__name__}"
        return getattr(Interpreter, method_name, Interpreter.no_visit_method)(
            node, context
        )

    @staticmethod
    def no_visit_method(node: Node, context: Context):
        raise Exception(f"No visit_{type(node).__name__} method defined!")

    @staticmethod
    def visit_NumberNode(node: NumberNode, context: Context) -> RTResult:
        return RTResult().success(Number(node.tok.value).set_context(context).set_pos(node.start_pos, node.end_pos))  # type: ignore

    @staticmethod
    def visit_StringNode(node: StringNode, context: Context) -> RTResult:
        return RTResult().success(String(node.tok.value).set_context(context).set_pos(node.start_pos, node.end_pos))  # type: ignore

    @staticmethod
    def visit_BooleanNode(node: BooleanNode, context: Context) -> RTResult:
        return RTResult().success(Boolean(node.tok.value == "true").set_context(context).set_pos(node.start_pos, node.end_pos))  # type: ignore

    @staticmethod
    def visit_NilNode(node: NilNode, context: Context) -> RTResult:
        return RTResult().success(
            Nil().set_context(context).set_pos(node.start_pos, node.end_pos)
        )

    @staticmethod
    def visit_BinaryOperatorNode(
        node: BinaryOperatorNode, context: Context
    ) -> RTResult:
        res = RTResult()

        left: Value = res.register(Interpreter.visit(node.left_node, context))
        if res.error:
            return res
        right: Value = res.register(Interpreter.visit(node.right_node, context))
        if res.error:
            return res

        def handle_assign(case):
            if isinstance(node.left_node, VariableAccessNode):
                var_name = node.left_node.var_name.value
                value = context.symbol_table.get(var_name).get_value()  # type:ignore

                if not value:
                    return res.failure(
                        ReferenceError(
                            f"{var_name} is not defined",
                            node.start_pos,
                            node.end_pos,
                            context,
                            generate_hint(context, var_name),
                        )
                    )

                expr = res.register(Interpreter.visit(node.right_node, context))
                if res.error:
                    return res

                expr = expr.get_value()

                if type(value) == str and type(expr) == str:
                    if node.op_tok.type == TT_SUMASSIGN:
                        value += expr

                    context.symbol_table.set(var_name, String(value))  # type: ignore
                    return String(value), None  # type: ignore

                else:
                    value = Switch(
                        node.op_tok.type,
                        [
                            ReturnableCase(TT_SUMASSIGN, value + expr),
                            ReturnableCase(TT_SUBASSIGN, value - expr),
                            ReturnableCase(TT_MULASSIGN, value * expr),
                            ReturnableCase(TT_DIVASSIGN, value / expr),
                            ReturnableCase(TT_POWASSIGN, value**expr),
                        ],
                    ).eval()

                context.symbol_table.set(var_name, Number(value))  # type: ignore
                return Number(value), None  # type: ignore

        result, error = Switch(
            node.op_tok.type,
            [
                ReturnableCase(TT_PLUS, left.added_to(right)),
                ReturnableCase(TT_MINUS, left.subtracted_by(right)),
                ReturnableCase(TT_MUL, left.multiplied_by(right)),
                ReturnableCase(TT_DIV, left.divided_by(right)),
                ReturnableCase(TT_POW, left.raised_to(right)),
                ReturnableCase(TT_EQL, left.comp_eq(right)),
                ReturnableCase(TT_NEQL, left.comp_neq(right)),
                ReturnableCase(TT_LT, left.comp_lt(right)),
                ReturnableCase(TT_GT, left.comp_gt(right)),
                ReturnableCase(TT_LTE, left.comp_lte(right)),
                ReturnableCase(TT_GTE, left.comp_gte(right)),
                AuxiliaryCase(
                    ((TT_KWRD, "and"),),
                    left.comp_and(right),
                    (node.op_tok.type, node.op_tok.value),
                ),
                AuxiliaryCase(
                    ((TT_KWRD, "or"),),
                    left.comp_or(right),
                    (node.op_tok.type, node.op_tok.value),
                ),
                ExecutableCase(
                    (
                        TT_SUMASSIGN,
                        TT_SUBASSIGN,
                        TT_MULASSIGN,
                        TT_DIVASSIGN,
                        TT_POWASSIGN,
                        TT_MODASSIGN,
                    ),
                    handle_assign,
                ),
            ],
        ).eval()  # type: ignore

        if error:
            return res.failure(error)

        return res.success(result.set_pos(node.start_pos, node.end_pos))

    @staticmethod
    def visit_UnaryOperatorNode(node: UnaryOperatorNode, context: Context) -> RTResult:
        res = RTResult()
        right: Value = res.register(Interpreter.visit(node.right_node, context))
        if res.error:
            return res

        error = None

        if node.op_tok.type == TT_MINUS and type(right) == Number:
            right, error = right.multiplied_by(Number(-1))  # type: ignore

        elif node.op_tok.matches(TT_KWRD, "not"):
            right, error = right.unary_not()  # type: ignore

        elif node.op_tok.type in (TT_INC, TT_DEC):
            var_name = node.right_node.var_name.value  # type: ignore
            value = context.symbol_table.get(var_name).get_value()  # type:ignore

            if value == None:
                # visit all parent symbol tables
                ctx = context
                list_of_vars = []
                hint = None

                while ctx:
                    list_of_vars.extend(ctx.symbol_table.symbols.keys())
                    ctx = ctx.parent

                best_match = rank(list_of_vars, str(var_name), 3.14159)
                if len(best_match) > 0:
                    best_match = best_match[0]
                    if int(best_match["score"]) / len(str(var_name)) >= 0.3:
                        hint = str(best_match["word"])

                if hint:
                    hint = f"Did you mean {hint}?"

                return res.failure(
                    ReferenceError(
                        f"{var_name} is not defined",
                        node.start_pos,
                        node.end_pos,
                        context,
                        hint,
                    )
                )

            right = Number(value + (1 if node.op_tok.type == TT_INC else -1))
            context.symbol_table.set(var_name, right)

        if error:
            return res.failure(error)

        return res.success(right.set_pos(node.start_pos, node.end_pos))

    @staticmethod
    def visit_FmtStringNode(node: FmtStringNode, context: Context):
        res = RTResult()
        final_str = ""

        for n in node.nodes:
            val = res.register(Interpreter.visit(n, context))
            if res.error:
                return res

            final_str += (
                val.__repr__(inc_quotes=False)
                if isinstance(val, String)
                else val.__repr__()
            )

        return res.success(String(final_str))

    @staticmethod
    def visit_VariableAccessNode(node: VariableAccessNode, context: Context):
        res = RTResult()
        var_name = node.var_name.value
        value = context.symbol_table.get(var_name)  # type:ignore

        if not value:
            # visit all parent symbol tables
            ctx = context

            return res.failure(
                ReferenceError(
                    f"{var_name} is not defined",
                    node.start_pos,
                    node.end_pos,
                    context,
                    generate_hint(context, var_name),
                )
            )

        value = value.copy().set_pos(node.start_pos, node.end_pos)
        return res.success(value)

    @staticmethod
    def visit_VariableInitNode(node: VariableInitNode, context: Context):
        res = RTResult()
        var_name = node.var_name.value
        if context.symbol_table.get(var_name):
            return res.failure(
                ReferenceError(
                    f"{var_name} was already declared",
                    node.start_pos,
                    node.end_pos,
                    context,
                )
            )

        value = res.register(Interpreter.visit(node.value, context))
        if res.error:
            return res

        context.symbol_table.set(var_name, value)

        return res.success(value)

    @staticmethod
    def visit_VariableAssignNode(node: VariableAssignNode, context: Context):
        res = RTResult()
        var_name = node.var_name.value
        if not context.symbol_table.get(var_name):
            return res.failure(
                ReferenceError(
                    f"{var_name} is undefined",
                    node.start_pos,
                    node.end_pos,
                    context,
                )
            )

        value = res.register(Interpreter.visit(node.value, context))
        if res.error:
            return res

        context.symbol_table.set(var_name, value)

        return res.success(value)

    @staticmethod
    def visit_IfNode(node: IfNode, context: Context):
        res = RTResult()

        for condition, expr in node.cases:
            condition_value = res.register(Interpreter.visit(condition, context))
            if res.error:
                return res

            if condition_value.is_true():
                expr_value = res.register(Interpreter.visit(expr, context))
                if res.error:
                    return res
                return res.success(expr_value)

        if node.else_case:
            else_value = res.register(Interpreter.visit(node.else_case, context))
            if res.error:
                return res
            return res.success(else_value)

        return res.success(
            Nil()
            .set_context(context)
            .set_pos(node.start_pos, node.start_pos.copy().advance().advance())
        )

    @staticmethod
    def visit_WhileNode(node: WhileNode, context: Context):
        res = RTResult()

        while True:
            condition = res.register(Interpreter.visit(node.condition, context))
            if res.error:
                return res

            if not condition.is_true():
                break

            res.register(Interpreter.visit(node.do, context))
            if res.error:
                return res

        return res

    @staticmethod
    def visit_FnDefNode(node: FnDefNode, context: Context):
        res = RTResult()

        name = node.var_name.value if node.var_name else None
        body = node.body
        arg_names = (
            [arg_name.value for arg_name in node.arg_names] if node.arg_names else []
        )

        fn_val = (
            Function(name, body, arg_names)
            .set_context(context)
            .set_pos(node.start_pos, node.end_pos)
        )

        if name:
            context.symbol_table.set(name, fn_val)

        return res.success(fn_val)

    @staticmethod
    def visit_CallNode(node: CallNode, context: Context):
        res = RTResult()
        args = []

        val_to_call = res.register(Interpreter.visit(node.to_call, context))
        if res.error:
            return res
        val_to_call = val_to_call.copy().set_pos(node.start_pos, node.end_pos)

        if node.args:
            for arg_node in node.args:
                args.append(res.register(Interpreter.visit(arg_node, context)))
                if res.error:
                    return res

        ret_val = res.register(val_to_call.execute(args))
        if res.error:
            return res

        return res.success(ret_val)
