from tok import Token
from constants import *
from position import Position
from parser_nodes import *
from error import *

class ParseResult:
    def __init__(self):
        self.error = None
        self.error_cache = None
        self.node = None
        self.advance_count = 0
        self.to_reverse_count = 0
        self.last_registered_advance_count = 0

    def register_advance(self):
        self.advance_count += 1

    def register(self, res):
        self.last_registered_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def try_register(self, res):
        if res.error:
            self.to_reverse_count = res.advance_count
            self.error_cache = res.error
            return None
        return self.register(res)

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        self.update_cur_tok()
        return self.cur_tok

    def reverse(self, amount=1):
        self.tok_idx -= amount
        self.update_cur_tok()
        return self.cur_tok

    def update_cur_tok(self):
        if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
            self.cur_tok = self.tokens[self.tok_idx]

    def parse(self):
        res = self.statements()

        if not res.error and self.cur_tok.type != TT_EOF:
            return res.failure(
                InvalidSyntax(
                    "Unexpected EOF",
                    self.cur_tok.start_pos,
                    self.cur_tok.end_pos,
                )
            )
        return res

    def statements(self):
        res = ParseResult()
        statements = []
        start_pos = self.cur_tok.start_pos.copy()
        more_statements = False

        while self.cur_tok.type == TT_NL:
            res.register_advance()
            self.advance()

        statement = res.register(self.statement())
        if res.error:
            return res
        statements.append(statement)

        more_statements = True


        while True:
            nl_count = 0

            while self.cur_tok.type == TT_NL:
                res.register_advance()
                self.advance()
                nl_count += 1

            if nl_count == 0:
                more_statements = False

            if not more_statements:
                break

            statement = res.try_register(self.statement())
            if res.error_cache and res.to_reverse_count > 0:
                res.error = res.error_cache
                self.advance()
                return res
            
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue


            statements.append(statement)
        
        return res.success(ListNode(statements, start_pos, self.cur_tok.end_pos.copy()))

    def statement(self) -> ParseResult:
        res = ParseResult()
        start_pos = self.cur_tok.start_pos.copy()

        if self.cur_tok.matches(TT_KWRD, "return"):
            res.register_advance()
            self.advance()

            expr_to_ret = res.try_register(self.expr())
            if not expr_to_ret:
                self.reverse(res.to_reverse_count)
            return res.success(ReturnNode(expr_to_ret, start_pos, self.cur_tok.end_pos))

        if self.cur_tok.matches(TT_KWRD, "continue"):
            res.register_advance()
            self.advance()

            return res.success(ContinueNode(start_pos, self.cur_tok.end_pos))

        if self.cur_tok.matches(TT_KWRD, "break"):
            res.register_advance()
            self.advance()

            return res.success(BreakNode(start_pos, self.cur_tok.end_pos))

        expr = res.register(self.expr())
        if res.error:
            return res
        return res.success(expr)

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
                if self.tok_idx + 1 < len(self.tokens):
                    if self.tokens[self.tok_idx + 1].type in (TT_IDENT, TT_KWRD):
                        hint = f"Identifiers can't begin with a number. Try removing the '{self.cur_tok.value}' at the beginning, or add an underscore infront of it"
                    else:
                        hint = f"Numbers can't be used as identifiers. Try changing '{self.cur_tok.value}' to a valid identifier, or add an underscore infront of it"

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
                if self.tokens[self.tok_idx + 1].type not in (
                    TT_ASSIGN,
                    TT_SUMASSIGN,
                    TT_SUBASSIGN,
                    TT_MULASSIGN,
                    TT_DIVASSIGN,
                    TT_POWASSIGN,
                    TT_MODASSIGN,
                    TT_INC,
                    TT_DEC,
                ):
                    return self.bin_op(
                        self.comp_expr, ((TT_KWRD, "and"), (TT_KWRD, "or"))
                    )

            res.register_advance()
            self.advance()
            if self.cur_tok.type in (
                TT_SUMASSIGN,
                TT_SUBASSIGN,
                TT_MULASSIGN,
                TT_DIVASSIGN,
                TT_POWASSIGN,
                TT_MODASSIGN,
            ):
                op_tok = self.cur_tok
                res.register_advance()
                self.advance()
                exp = res.register(self.expr())
                if res.error:
                    return res

                return res.success(
                    BinaryOperatorNode(VariableAccessNode(var_name), op_tok, exp)
                )

            if self.cur_tok.type in (TT_INC, TT_DEC):
                op_tok = self.cur_tok
                res.register_advance()
                self.advance()
                return res.success(
                    UnaryOperatorNode(op_tok, VariableAccessNode(var_name))
                )

            if self.cur_tok.type != TT_ASSIGN:
                if not init:
                    return self.bin_op(
                        self.comp_expr, ((TT_KWRD, "and"), (TT_KWRD, "or"))
                    )
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
                    f"Unexpected token of type {self.cur_tok.type}",
                    self.cur_tok.start_pos,
                    self.cur_tok.end_pos,
                )
            )

        return res.success(node)

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
            self.bin_op(self.arith_expr, (TT_EQL, TT_LT, TT_GT, TT_LTE, TT_GTE, (TT_KWRD, "in")))
        )

        if res.error:
            return res.failure(
                InvalidSyntax(
                    f"Unexpected token of type {self.cur_tok.type}",
                    self.cur_tok.start_pos,
                    self.cur_tok.end_pos,
                )
            )

        return res.success(node)

    def arith_expr(self) -> ParseResult:
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS, TT_AT))

    def term(self) -> ParseResult:
        return self.bin_op(self.factor, (TT_MUL, TT_DIV, TT_FLRDIV, TT_MOD))

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

    def power(self) -> ParseResult:
        return self.bin_op(self.call, (TT_POW,), right_func=self.factor)

    def call(self) -> ParseResult:
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error:
            return res

        if self.cur_tok.type == TT_LPAREN:
            res.register_advance()
            self.advance()

            arg_nodes = []

            if self.cur_tok.type == TT_RPAREN:
                res.register_advance()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(
                        InvalidSyntax(
                            f"Unexpected token of type {self.cur_tok.type}",
                            self.cur_tok.start_pos,
                            self.cur_tok.end_pos,
                        )
                    )

                while self.cur_tok.type == TT_COMMA:
                    res.register_advance()
                    self.advance()
                    arg_nodes.append(res.register(self.expr()))
                    if res.error:
                        return res

                if self.cur_tok.type != TT_RPAREN:
                    return res.failure(
                        InvalidSyntax(
                            f"Expected ')', got {self.cur_tok.type}",
                            self.cur_tok.start_pos,
                            self.cur_tok.end_pos,
                        )
                    )

                res.register_advance()
                self.advance()

            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)

    def atom(self):
        res = ParseResult()
        tok = self.cur_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advance()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == TT_STRING:
            res.register_advance()
            self.advance()
            return res.success(StringNode(tok))

        elif (tok.type, tok.value) in ((TT_KWRD, "true"), (TT_KWRD, "false")):
            res.register_advance()
            self.advance()
            return res.success(BooleanNode(tok))

        elif tok.matches(TT_KWRD, "nil"):
            res.register_advance()
            self.advance()
            return res.success(NilNode(tok))

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
                        f"Expected ')', got {self.cur_tok.type}",
                        self.cur_tok.start_pos,
                        self.cur_tok.end_pos,
                        "Try adding a ')' where indicated",
                    )
                )

        elif tok.type == TT_LBRACK:
            list_expr = res.register(self.list_expr())
            if res.error:
                return res
            return res.success(list_expr)

        elif tok.type == TT_IDENT:
            res.register_advance()
            self.advance()
            return res.success(VariableAccessNode(tok))

        elif tok.type == TT_FMT_STRING:
            fmt_string = res.register(self.fmt_string_expr())
            if res.error:
                return res
            return res.success(fmt_string)

        elif tok.matches(TT_KWRD, "if"):
            if_expr = res.register(self.if_expr())
            if res.error:
                return res
            return res.success(if_expr)

        elif tok.matches(TT_KWRD, "while"):
            while_expr = res.register(self.while_expr())
            if res.error:
                return res
            return res.success(while_expr)

        elif tok.matches(TT_KWRD, "fn"):
            fn_expr = res.register(self.fn_def())
            if res.error:
                return res
            return res.success(fn_expr)

        return res.failure(
            InvalidSyntax(
                f"Unexpected token of type {self.cur_tok.type}",
                tok.start_pos,
                tok.end_pos,
            )
        )

    def list_expr(self):
        res = ParseResult()
        element_nodes = []
        start_pos = self.cur_tok.start_pos.copy()
        if self.cur_tok.type != TT_LBRACK:
            return res.failure(
                InvalidSyntax(
                    f"Expected '[', got {self.cur_tok.type}",
                    start_pos,
                    self.cur_tok.end_pos.copy(),
                )
            )

        res.register_advance()
        self.advance()

        if self.cur_tok.type == TT_RBRACK:
            res.register_advance()
            self.advance()
        else:
            element_nodes.append(res.register(self.expr()))
            if res.error:
                return res.failure(
                    InvalidSyntax(
                        f"Unexpected token of type {self.cur_tok.type}",
                        self.cur_tok.start_pos,
                        self.cur_tok.end_pos,
                    )
                )

            while self.cur_tok.type == TT_COMMA:
                res.register_advance()
                self.advance()
                element_nodes.append(res.register(self.expr()))
                if res.error:
                    return res

            if self.cur_tok.type != TT_RBRACK:
                return res.failure(
                    InvalidSyntax(
                        f"Expected ']', got {self.cur_tok.type}",
                        self.cur_tok.start_pos,
                        self.cur_tok.end_pos,
                    )
                )

            res.register_advance()
            self.advance()

        return res.success(
            ListNode(element_nodes, start_pos, self.cur_tok.end_pos.copy())
        )

    def fmt_string_expr(self):
        res = ParseResult()
        tok = self.cur_tok
        parsed_nodes = []

        if self.cur_tok.type == TT_FMT_STRING:
            for node_to_parse in self.cur_tok.value:
                if node_to_parse[1] == "string":
                    parsed_nodes.append(StringNode(node_to_parse[0]))
                elif node_to_parse[1] == "expr":
                    if node_to_parse[0][0].type == TT_EOF:
                        continue

                    parser = Parser(node_to_parse[0])
                    new_res = parser.parse()

                    if new_res.error:
                        return new_res
                    parsed_nodes.append(new_res.node)  # type:ignore

        res.register_advance()
        self.advance()
        if parsed_nodes:
            return res.success(FmtStringNode(parsed_nodes))
        else:
            return res.failure(
                InvalidSyntax(
                    "Formatted string cannot be empty",
                    tok.start_pos,
                    tok.end_pos,
                )
            )

    def if_or_elif_expr(self, kwrd):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.cur_tok.matches(TT_KWRD, kwrd):
            return res.failure(
                InvalidSyntax(
                    f"Expected '{kwrd}', got {self.cur_tok.type}",
                    self.cur_tok.start_pos,
                    self.cur_tok.end_pos,
                )
            )

        res.register_advance()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if not self.cur_tok.matches(TT_KWRD, "then"):
            return res.failure(
                InvalidSyntax(
                    "Expected 'then', got {self.cur_tok.type}",
                    self.cur_tok.start_pos,
                    self.cur_tok.end_pos,
                )
            )

        res.register_advance()
        self.advance()

        if self.cur_tok.type == TT_NL:
            res.register_advance()
            self.advance()

            statements = res.register(self.statements())
            if res.error:
                return res
            cases.append((condition, statements, True))

            if self.cur_tok.matches(TT_KWRD, "end"):
                res.register_advance()
                self.advance()
            else:
                all_cases = res.register(self.elif_or_else_expr())
                if res.error:
                    return res
                new_cases, else_case = all_cases  # type:ignore
                cases.extend(new_cases)

        else:
            expr = res.register(self.statement())
            if res.error:
                return res
            cases.append((condition, expr, False))

            all_cases = res.register(self.elif_or_else_expr())
            if res.error:
                return res
            new_cases, else_case = all_cases  # type:ignore
            cases.extend(new_cases)

        return res.success((cases, else_case))  # type:ignore

    def if_expr(self):
        res = ParseResult()
        all_cases = res.register(self.if_or_elif_expr("if"))
        if res.error:
            return res
        cases, else_case = all_cases  # type:ignore
        return res.success(IfNode(cases, else_case))

    def elif_expr(self):
        return self.if_or_elif_expr("elif")

    def else_expr(self):
        res = ParseResult()
        else_case = None

        if self.cur_tok.matches(TT_KWRD, "else"):
            res.register_advance()
            self.advance()

            if self.cur_tok.type == TT_NL:
                res.register_advance()
                self.advance()

                statements = res.register(self.statements())
                if res.error:
                    return res
                else_case = (statements, True)

                if self.cur_tok.matches(TT_KWRD, "end"):
                    res.register_advance()
                    self.advance()
                else:
                    return res.failure(
                        InvalidSyntax(
                            f"Expected 'end', got {self.cur_tok.type}",
                            self.cur_tok.start_pos,
                            self.cur_tok.end_pos,
                        )
                    )
            else:
                expr = res.register(self.statement())
                if res.error:
                    return res
                else_case = (expr, False)

        return res.success(else_case)  # type:ignore

    def elif_or_else_expr(self):
        res = ParseResult()
        cases, else_case = [], None

        if self.cur_tok.matches(TT_KWRD, "elif"):
            all_cases = res.register(self.elif_expr())
            if res.error:
                return res
            cases, else_case = all_cases  # type:ignore

        else:
            else_case = res.register(self.else_expr())
            if res.error:
                return res

        return res.success((cases, else_case))  # type:ignore

    def while_expr(self):
        res = ParseResult()

        if not self.cur_tok.matches("KWRD", "while"):
            return res.failure(
                InvalidSyntax(
                    f"Expected 'while', got {self.cur_tok.type}",
                    self.cur_tok.start_pos,
                    self.cur_tok.end_pos,
                )
            )

        res.register_advance()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if not self.cur_tok.matches("KWRD", "do"):
            return res.failure(
                InvalidSyntax(
                    f"Expected 'do', got {self.cur_tok.type}",
                    self.cur_tok.start_pos,
                    self.cur_tok.end_pos,
                )
            )

        res.register_advance()
        self.advance()

        if self.cur_tok.type == TT_NL:
            res.register_advance()
            self.advance()

            body = res.register(self.statements())
            if res.error:
                return res

            if not self.cur_tok.matches(TT_KWRD, "end"):
                return res.failure(
                    InvalidSyntax(
                        f"Expected 'end', got {self.cur_tok.type}",
                        self.cur_tok.start_pos,
                        self.cur_tok.end_pos,
                    )
                )

            res.register_advance()
            self.advance()

            return res.success(WhileNode(condition, body, True))

        body = res.register(self.statement())
        if res.error:
            return res

        return res.success(WhileNode(condition, body, False))

    def fn_def(self):
        res = ParseResult()
        is_anonymous = True

        if not self.cur_tok.matches("KWRD", "fn"):
            return res.failure(
                InvalidSyntax(
                    f"Expected 'fn', got {self.cur_tok.type}",
                    self.cur_tok.start_pos,
                    self.cur_tok.end_pos,
                )
            )

        res.register_advance()
        self.advance()

        var_name = None
        arg_names = []

        if self.cur_tok.type == TT_IDENT:
            var_name = self.cur_tok
            is_anonymous = False
            res.register_advance()
            self.advance()

        if self.cur_tok.type == TT_LPAREN:
            res.register_advance()
            self.advance()

            if self.cur_tok.type == TT_IDENT:
                arg_names.append(self.cur_tok)
                res.register_advance()
                self.advance()

                while self.cur_tok.type == TT_COMMA:
                    res.register_advance()
                    self.advance()

                    if self.cur_tok.type != TT_IDENT:
                        return res.failure(
                            InvalidSyntax(
                                f"Expected identifier, got {self.cur_tok.type}",
                                self.cur_tok.start_pos,
                                self.cur_tok.end_pos,
                            )
                        )
                    arg_names.append(self.cur_tok)
                    res.register_advance()
                    self.advance()

                if self.cur_tok.type != TT_RPAREN:
                    return res.failure(
                        InvalidSyntax(
                            f"Expected ',' or ')', got {self.cur_tok.type}",
                            self.cur_tok.start_pos,
                            self.cur_tok.end_pos,
                        )
                    )

                res.register_advance()
                self.advance()

        if is_anonymous:
            if self.cur_tok.type != TT_ARROW:
                return res.failure(
                    InvalidSyntax(
                        f"Expected => in anonymous function definition, got {self.cur_tok.type}",
                        self.cur_tok.start_pos,
                        self.cur_tok.end_pos,
                    )
                )

            res.register_advance()
            self.advance()

            body = res.register(self.expr())
            if res.error:
                return res

            return res.success(
                FnDefNode(
                    var_name, arg_names if len(arg_names) > 0 else None, body, True
                )
            )

        else:
            if not self.cur_tok.matches(TT_KWRD, "do"):
                return res.failure(
                    InvalidSyntax(
                        f"Expected 'do', got {self.cur_tok.type}",
                        self.cur_tok.start_pos,
                        self.cur_tok.end_pos,
                    )
                )

            res.register_advance()
            self.advance()

            body = res.register(self.statements())
            
            if res.error:
                return res
            
            while self.cur_tok.type == TT_NL:
                res.register_advance()
                self.advance()

            if not is_anonymous and not self.cur_tok.matches(TT_KWRD, "end"):
                return res.failure(
                    InvalidSyntax(
                        f"Expected 'end', got {self.cur_tok.type}",
                        self.cur_tok.start_pos,
                        self.cur_tok.end_pos,
                    )
                )
            
            res.register_advance()
            self.advance()
            
            return res.success(
                FnDefNode(
                    var_name, arg_names if len(arg_names) > 0 else None, body, False
                )
            )

    def bin_op(self, func, ops, right_func=None):
        res = ParseResult()
        left = res.register(func())
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
