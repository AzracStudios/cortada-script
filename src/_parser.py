from tok import Token
from constants import *
from position import Position
from parser_nodes import *
from error import *
from typing import Self, Any


class ParseResult:
    def __init__(self):
        self.error: Error | None = None
        self.node: Node | None = None
        self.advance_count = 0

    def register_advance(self) -> None:
        self.advance_count += 1

    def register(self, res: Self) -> Node:
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node  # type: ignore

    def success(self, node: Node) -> Self:
        self.node = node
        return self

    def failure(self, error: Error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1

        if self.tok_idx < len(self.tokens):
            self.cur_tok = self.tokens[self.tok_idx]

        return self.cur_tok

    def parse(self):
        res: ParseResult = self.expr()
        if not res.error and self.cur_tok.type != TT_EOF:
            return res.failure(
                InvalidSyntax(
                    "Unexpected EOF",
                    self.cur_tok.start_pos,
                    self.cur_tok.end_pos,
                )
            )
        return res

    def atom(self):
        res = ParseResult()
        tok = self.cur_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advance()
            self.advance()
            return res.success(NumberNode(tok))

        if (tok.type, tok.value) in ((TT_KWRD, "true"), (TT_KWRD, "false")):
            res.register_advance()
            self.advance()
            return res.success(BooleanNode(tok))

        elif tok.type == TT_LPAREN:
            res.register_advance()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res

            if self.cur_tok.type == TT_RPAREN:
                res.register_advance()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(
                    InvalidSyntax(
                        "Expected ')'",
                        self.cur_tok.start_pos,
                        self.cur_tok.end_pos,
                        "Try adding a ')' where indicated",
                    )
                )

        elif tok.type == TT_IDENT:
            res.register_advance()
            self.advance()
            return res.success(VariableAccessNode(tok))

        return res.failure(
            InvalidSyntax(
                f"Expected int, float, identifier, '+', '-' or '(', got {tok.type}",
                tok.start_pos,
                tok.end_pos,
            )
        )

    def power(self) -> ParseResult:
        return self.bin_op(self.atom, (TT_POW,), right_func=self.factor)

    def factor(self) -> ParseResult:
        res = ParseResult()
        tok = self.cur_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advance()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOperatorNode(tok, factor))

        return self.power()

    def term(self) -> ParseResult:
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def arith_expr(self) -> ParseResult:
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def comp_expr(self) -> ParseResult:
        res = ParseResult()

        if self.cur_tok.matches(TT_KWRD, "not"):
            op_tok = self.cur_tok
            res.register_advance()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error:
                return res
            return res.success(UnaryOperatorNode(op_tok, node))

        node = res.register(
            self.bin_op(self.arith_expr, (TT_EQL, TT_LT, TT_GT, TT_LTE, TT_GTE))
        )
        if res.error:
            return res.failure(
                InvalidSyntax(
                    f"Expected int, float, identifier, '+', '-', '(' or 'not' got {self.cur_tok.type}",
                    self.cur_tok.start_pos,
                    self.cur_tok.end_pos,
                )
            )

        return res.success(node)

    def expr(self) -> ParseResult:
        res = ParseResult()
        init = False

        if self.cur_tok.matches(TT_KWRD, "var"):
            res.register_advance()
            self.advance()
            init = True

        if self.cur_tok.type != TT_IDENT and init:
            hint = None

            if self.cur_tok.type in (TT_INT, TT_FLOAT):
                hint = f"Identifiers can't begin with a number. Try removing the '{self.cur_tok.value}' at the beginning, or add an underscore infront of it"

            return res.failure(
                InvalidSyntax(
                    f"Expected identifier, got {self.cur_tok.type}",
                    self.cur_tok.start_pos,
                    self.cur_tok.end_pos,
                    hint,
                )
            )

        if self.cur_tok.type == TT_IDENT:
            var_name = self.cur_tok
            if self.tok_idx + 1 < len(self.tokens) and not init:
                if self.tokens[self.tok_idx + 1].type != TT_ASSIGN:
                    return self.bin_op(
                        self.comp_expr, ((TT_KWRD, "and"), (TT_KWRD, "or"))
                    )

            res.register_advance()
            self.advance()
            if self.cur_tok.type != TT_ASSIGN and init:
                return res.failure(
                    InvalidSyntax(
                        f"Expected '=', got {self.cur_tok.type}",
                        self.cur_tok.start_pos,
                        self.cur_tok.end_pos,
                    )
                )

            res.register_advance()
            self.advance()

            expr = res.register(self.expr())
            if res.error:
                return res

            return res.success(
                VariableInitNode(var_name, expr)
                if init
                else VariableAssignNode(var_name, expr)
            )

        node = res.register(
            self.bin_op(self.comp_expr, ((TT_KWRD, "and"), (TT_KWRD, "or")))
        )
        if res.error:
            return res.failure(
                InvalidSyntax(
                    f"Expected int, float, identifier, 'var', '+', '-' or '(', got {self.cur_tok.type}",
                    self.cur_tok.start_pos,
                    self.cur_tok.end_pos,
                )
            )

        return res.success(node)

    def bin_op(self, func, ops, right_func=None):
        res = ParseResult()
        left: Node = res.register(func())
        if res.error:
            return res

        while (
            self.cur_tok.type in ops or (self.cur_tok.type, self.cur_tok.value) in ops
        ):
            op_tok = self.cur_tok
            res.register_advance()
            self.advance()
            right = res.register(func() if not right_func else right_func())
            if res.error:
                return res
            left = BinaryOperatorNode(left, op_tok, right)

        return res.success(left)
