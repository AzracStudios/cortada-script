from parser_nodes import *
from rtval import *
from switch import *
from constants import *
from error import Error
from context import Context
from rank import rank


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


class Interpreter:
    def visit(self, node: Node, context: Context) -> RTResult:
        method_name = f"visit_{type(node).__name__}"
        return getattr(self, method_name, self.no_visit_method)(node, context)

    def no_visit_method(self, node: Node, context: Context):
        raise Exception(f"No visit_{type(node).__name__} method defined!")

    def visit_NumberNode(self, node: NumberNode, context: Context) -> RTResult:
        return RTResult().success(Number(node.tok.value).set_context(context).set_pos(node.start_pos, node.end_pos))  # type: ignore

    def visit_BooleanNode(self, node: BooleanNode, context: Context) -> RTResult:
        return RTResult().success(Boolean(node.tok.value == 'true').set_context(context).set_pos(node.start_pos, node.end_pos))  # type: ignore

    def visit_BinaryOperatorNode(
        self, node: BinaryOperatorNode, context: Context
    ) -> RTResult:
        res = RTResult()

        left: Value = res.register(self.visit(node.left_node, context))
        if res.error:
            return res
        right: Value = res.register(self.visit(node.right_node, context))
        if res.error:
            return res

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
            ],
        ).eval()  # type: ignore

        if error:
            return res.failure(error)

        return res.success(result.set_pos(node.start_pos, node.end_pos))

    def visit_UnaryOperatorNode(
        self, node: UnaryOperatorNode, context: Context
    ) -> RTResult:
        res = RTResult()
        right: Value = res.register(self.visit(node.right_node, context))
        if res.error:
            return res

        error = None

        if node.op_tok.type == TT_MINUS and type(right) == Number:
            right, error = right.multiplied_by(Number(-1))  # type: ignore
        elif node.op_tok.matches(TT_KWRD, "not"):
            right, error = right.unary_not() # type: ignore

        if error:
            return res.failure(error)

        return res.success(right.set_pos(node.start_pos, node.end_pos))

    def visit_VariableAccessNode(self, node: VariableAccessNode, context: Context):
        res = RTResult()
        var_name = node.var_name.value
        value = context.symbol_table.get(var_name)  # type:ignore

        if not value:
            # visit all parent symbol tables
            ctx = context
            list_of_vars = []
            hint = None

            while ctx:
                list_of_vars.extend(ctx.symbol_table.symbols.keys())
                ctx = ctx.parent

            best_match = rank(list_of_vars, str(var_name), 3.14159)[0]
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

        value = value.copy().set_pos(node.start_pos, node.end_pos)
        return res.success(value)

    def visit_VariableInitNode(self, node: VariableInitNode, context: Context):
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

        value = res.register(self.visit(node.value, context))
        if res.error:
            return res

        context.symbol_table.set(var_name, value)

        return res.success(value)

    def visit_VariableAssignNode(self, node: VariableAssignNode, context: Context):
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

        value = res.register(self.visit(node.value, context))
        if res.error:
            return res

        context.symbol_table.set(var_name, value)

        return res.success(value)
