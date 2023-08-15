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

    def register(self, res: Any) -> Node:
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            ##! I have no clue on how to fix the following line without breaking the rest of the code
            ##! If anyone reading this has any idea please submit a pr, thanks in advance :)
            return res.node  # type: ignore
        return res

    def success(self, node: Node) -> Self:
        self.node = node
        return self

    def failure(self, error: Error):
        self.error = error
        return self


class Parser:
    def __init__(self, tokens: list[Token], src: str):
        self.tokens: list[Token] = tokens
        self.src = src
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
                InvalidSyntaxError(
                    self.src,
                    "Unexpected EOF",
                    self.cur_tok.start_pos,
                    self.cur_tok.end_pos,
                )
            )
        return res

    def factor(self) -> ParseResult:
        res = ParseResult()
        tok = self.cur_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOperatorNode(tok, factor))

        elif tok.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))

        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error:
                return res

            if self.cur_tok.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(
                    InvalidSyntaxError(
                        self.src,
                        "Expected ')'",
                        self.cur_tok.start_pos,
                        self.cur_tok.end_pos,
                        "Try adding a ')' where indicated",
                    )
                )

        return res.failure(
            InvalidSyntaxError(
                self.src,
                f"Expected int or float, got {tok.type}",
                tok.start_pos,
                tok.end_pos,
            )
        )

    def term(self) -> ParseResult:
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def expr(self) -> ParseResult:
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def bin_op(self, func, ops):
        res = ParseResult()
        left: Node = res.register(func())
        if res.error:
            return res

        while self.cur_tok.type in ops:
            op_tok = self.cur_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error:
                return res
            left = BinaryOperatorNode(left, op_tok, right)

        return res.success(left)
