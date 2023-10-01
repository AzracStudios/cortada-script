from position import Position
from tok import Token
from error import IllegalCharacter, UnterminatedString, Error
from switch import *
from constants import *
from color import Colors


class Lexer:
    def __init__(self, file_name, src):
        self.file_name = file_name
        self.src = src
        self.char = ""
        self.position = Position(-1, -1, 0, self.file_name, self.src)
        self.should_advance_next_ittr = True
        self.tokens = []
        self.advance()

    def advance(self):
        self.position.advance(self.char)

        if self.position.idx < len(self.src):
            self.char = self.src[self.position.idx]
            return

        self.char = None

    def case_has_assignment(self, case):
        pos = self.position.copy()
        assign_case_lut = {
            "%": TT_MOD,
            "%=": TT_MODASSIGN,
            "=": TT_ASSIGN,
            "==": TT_EQL,
            "!=": TT_NEQL,
            "<": TT_LT,
            "<=": TT_LTE,
            ">": TT_GT,
            ">=": TT_GTE,
        }

        self.advance()
        if self.char == "=":
            return Token(assign_case_lut[f"{case}="], pos, end_pos=self.position)
        if self.char == ">":
            return Token(TT_ARROW, pos, end_pos=self.position)

        self.should_advance_next_ittr = False
        return Token(assign_case_lut[case], pos)

    def case_has_assignment_or_repeats(self, case: str) -> Token | None:
        pos = self.position.copy()
        assign_repeat_case_lut = {
            "+": TT_PLUS,
            "++": TT_INC,
            "+=": TT_SUMASSIGN,
            "-": TT_MINUS,
            "--": TT_DEC,
            "-=": TT_SUBASSIGN,
            "*": TT_MUL,
            "**": TT_POW,
            "*=": TT_MULASSIGN,
            "/": TT_DIV,
            "//": TT_FLRDIV,
            "/=": TT_DIVASSIGN,
        }

        if case not in assign_repeat_case_lut:
            return None

        self.advance()

        if self.char == "=":
            return Token(assign_repeat_case_lut[f"{case}="], pos, end_pos=self.position)

        elif self.char == case:
            return Token(assign_repeat_case_lut[case * 2], pos, end_pos=self.position)

        self.should_advance_next_ittr = False
        return Token(assign_repeat_case_lut[case], pos)

    def case_num(self, case: str) -> Token | IllegalCharacter:
        pos = self.position.copy()
        num_str = ""
        is_float = case == "."
        should_return_error = False
        error_pos = None

        while self.char and self.char in NUM_STR:
            if self.char == ".":
                if is_float and not should_return_error:
                    should_return_error = True
                    error_pos = self.position.copy()
                num_str += "."
                is_float = True
                self.advance()
                continue

            num_str += self.char
            self.advance()

        self.should_advance_next_ittr = False

        if should_return_error:
            return IllegalCharacter(
                ".",
                pos,
                self.position.copy(),
                help_text=f"{Colors.bright_green(num_str)} is not a valid int or float. Try removing the '.' @ {error_pos}",
            )

        return Token(
            TT_FLOAT if is_float else TT_INT,
            pos,
            value=float(num_str) if is_float else int(num_str),
            end_pos=self.position,
        )

    def case_kwrd_or_ident(self, case):
        pos = self.position.copy()
        kwrd_ident_str = ""

        while self.char and (self.char in (ALPH_STR + NUM_STR + "_")) and self.char != " ":
            kwrd_ident_str += self.char
            self.advance()

        self.should_advance_next_ittr = False

        return Token(
            TT_KWRD if kwrd_ident_str in KWRDS else TT_IDENT,
            pos,
            value=kwrd_ident_str,
            end_pos=self.position,
        )

    def case_string(self, case):
        pos = self.position.copy()
        esc = False

        if case in "\"'":
            self.advance()

        _str = ""

        esc_char = {"n": "\n", "t": "\t", "r": "\r", "b": "\b"}

        while (self.char != case or esc) and self.char != None:
            if esc:
                _str += esc_char.get(self.char, self.char)

            else:
                if self.char == "\\":
                    esc = True
                    self.advance()
                    continue
                else:
                    _str += self.char
            self.advance()
            esc = False

        if self.char != case:
            return UnterminatedString(pos, self.position.copy(), case)

        return Token("STRING", pos, end_pos=self.position, value=_str)

    def case_fmt_string(self, case):
        pos = self.position.copy()
        esc = False

        if case in "`":
            self.advance()

        fmt_str = []
        segment = ""

        esc_char = {"n": "\n", "t": "\t", "r": "\r", "b": "\b"}

        while (self.char != case or esc) and self.char != None:
            if esc:
                segment += esc_char.get(self.char, self.char)

            elif self.char == "$":
                self.advance()

                if self.char == "{":
                    self.advance()
                    if len(segment):
                        fmt_str.append((Token(TT_STRING, pos, value=segment), "string"))
                    segment = ""

                    toks: list[Token] = []
                    did_close = False

                    while self.char != None and self.char != "`":
                        if self.char == "}":
                            did_close = True
                            break

                        next_token, error = self.next()

                        if error:
                            if self.char == "$":
                                return Error(
                                    "Cannot nest formatted strings",
                                    self.src,
                                    pos,
                                    self.position,
                                    "Lexer Error",
                                )
                            return error

                        if self.should_advance_next_ittr:
                            self.advance()

                        if next_token and next_token != "SPACE":
                            toks.append(next_token)

                        self.should_advance_next_ittr = True

                    if self.char == "`" and not did_close:
                        return Error(
                            "Unexpected end of formatted string",
                            self.src,
                            pos,
                            self.position,
                            "Lexer Error",
                            help_text="Close the '${' with a '}'",
                        )

                    toks.append(Token(TT_EOF, self.position))
                    fmt_str.append((toks, "expr"))

                else:
                    segment += "$"
            else:
                if self.char == "\\":
                    esc = True
                    self.advance()
                    continue
                else:
                    segment += self.char

            if self.char != case:
                self.advance()
            esc = False

        if self.char != case:
            return UnterminatedString(pos, self.position.copy(), "`")
        elif segment != "":
            fmt_str.append((Token(TT_STRING, pos, value=segment), "string"))

        if self.char == case:
            self.advance()
        self.should_advance_next_ittr = False
        return Token(TT_FMT_STRING, pos, end_pos=self.position, value=fmt_str)

    def case_comment(self,case):
        while self.char != "\n":
            self.advance()
        
        return Token(TT_NL, self.position)
        
    def next(self):
        switch: Switch = Switch(
            self.char,
            [
                ReturnableCase(";\n", Token(TT_NL, self.position)),
                ReturnableCase("(", Token(TT_LPAREN, self.position)),
                ReturnableCase(")", Token(TT_RPAREN, self.position)),
                ReturnableCase("[", Token(TT_LBRACK, self.position)),
                ReturnableCase("]", Token(TT_RBRACK, self.position)),
                ReturnableCase("{", Token(TT_LBRACE, self.position)),
                ReturnableCase("}", Token(TT_RBRACE, self.position)),
                ReturnableCase(",", Token(TT_COMMA, self.position)),
                ReturnableCase("@", Token(TT_AT, self.position)),
                ReturnableCase(" \t", TT_SPACE),  # This is not added to the tokens list
                ExecutableCase(";~", self.case_comment),
                ExecutableCase("%=<>", self.case_has_assignment),
                ExecutableCase("`", self.case_fmt_string),
                ExecutableCase("+-*/", self.case_has_assignment_or_repeats),
                ExecutableCase(NUM_STR, self.case_num),
                ExecutableCase(f"_{ALPH_STR}", self.case_kwrd_or_ident),
                ExecutableCase("'\"", self.case_string),
            ],
        )

        tok = switch.eval()
        if isinstance(tok, Error):
            return (None, tok)

        if not tok:
            return (
                None,
                IllegalCharacter(
                    self.char,
                    self.position.copy(),
                    self.position.copy().advance(),
                ),
            )

        return (tok, None)

    def tokenize(self):
        while self.char != None:
            next_token, error = self.next()

            if error:
                return error

            if self.should_advance_next_ittr:
                self.advance()

            if next_token and next_token != "SPACE":
                self.tokens.append(next_token)

            self.should_advance_next_ittr = True

        self.tokens.append(Token(TT_EOF, self.position))
        return self.tokens
