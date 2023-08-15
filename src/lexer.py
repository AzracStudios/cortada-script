from position import Position
from tok import Token
from error import IllegalCharacterError
from switch import *
from constants import *
from color import Colors
from type import *


class Lexer:
    def __init__(self, file_name: str, src: str):
        self.file_name: str = file_name
        self.src: str = src
        self.char: str | None = ""
        self.position: Position = Position(-1, -1, 0, self.file_name)
        self.should_advance_next_ittr: bool = True
        self.tokens: list[Token] = []
        self.advance()

    def advance(self) -> None:
        self.position.advance(self.char)

        if self.position.idx < len(self.src):
            self.char = self.src[self.position.idx]
            return

        self.char = None

    def case_has_assignment(self, case: str) -> Token:
        pos = self.position.copy()
        assign_case_lut: dict[str, TokenType] = {
            "%": TT_MOD,
            "%=": TT_MODASSIGN,
            "=": TT_ASSIGN,
            "==": TT_EQL,
            "<": TT_LT,
            "<=": TT_LTE,
            ">": TT_GT,
            ">=": TT_GTE,
        }

        self.advance()
        if self.char == "=":
            return Token(assign_case_lut[f"{case}="], pos, end_pos=self.position)

        self.should_advance_next_ittr = False
        return Token(assign_case_lut[case], pos)

    def case_has_assignment_or_repeats(self, case: str) -> Token | None:
        pos = self.position.copy()
        assign_repeat_case_lut: dict[str, TokenType] = {
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

    def case_num(self, case: str) -> Token | IllegalCharacterError:
        pos = self.position.copy()
        num_str = ""
        is_float = case == "."
        should_return_error = False
        error_pos: Position | None = None

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
            return IllegalCharacterError(
                ".",
                self.src,
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
        should_return_error = False
        error_pos: Position | None = None
        error_char: str = ""

        while self.char and self.char != " ":
            kwrd_ident_str += self.char
            if (self.char not in (ALPH_STR + NUM_STR) or self.char == ".") and (
                not should_return_error
            ):
                error_pos = self.position.copy()
                should_return_error = True
                error_char = self.char
            self.advance()

        self.should_advance_next_ittr = False

        if should_return_error:
            return IllegalCharacterError(
                ".",
                self.src,
                pos,
                self.position.copy(),
                help_text=f"{Colors.bright_green(kwrd_ident_str)} is not a valid identifier. Try removing the '{error_char}' @ {error_pos}",
            )

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

        esc_char = {"n": "\n", "t": "\t"}

        while (self.char != case or esc) and self.char != None:
            if esc:
                _str += esc_char.get(self.char, self.char)
            else:
                if self.char == "\\":
                    esc = True
                else:
                    _str += self.char
            self.advance()
            esc = False

        self.should_advance_next_ittr = False

        return Token("STRING", pos, end_pos=self.position, value=_str)

    def next(self) -> tuple[Token | None, IllegalCharacterError | None]:
        switch: Switch = Switch(
            self.char,
            [
                ReturnableCase("(", Token(TT_LPAREN, self.position)),
                ReturnableCase(")", Token(TT_RPAREN, self.position)),
                ReturnableCase("[", Token(TT_LBRACK, self.position)),
                ReturnableCase("]", Token(TT_RBRACK, self.position)),
                ReturnableCase("{", Token(TT_LBRACE, self.position)),
                ReturnableCase("}", Token(TT_RBRACE, self.position)),
                ReturnableCase("\n", TT_NL),
                ReturnableCase(" ", TT_SPACE),  # This is not added to the tokens list
                ExecutableCase("%=<>", self.case_has_assignment),
                ExecutableCase("+-*/", self.case_has_assignment_or_repeats),
                ExecutableCase(NUM_STR, self.case_num),
                ExecutableCase(f"_{ALPH_STR}", self.case_kwrd_or_ident),
                ExecutableCase("'\"", self.case_string),
            ],
        )

        tok = switch.eval()
        if isinstance(tok, IllegalCharacterError):
            return (None, tok)

        if not tok:
            return (
                None,
                IllegalCharacterError(
                    self.char,
                    self.src,
                    self.position.copy(),
                    self.position.copy().advance(),
                ),
            )

        return (tok, None)

    def tokenize(self) -> list[Token] | IllegalCharacterError:
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
