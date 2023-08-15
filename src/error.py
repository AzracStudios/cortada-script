from position import Position
from color import Colors
from type import ErrorType


class Error:
    def __init__(
        self,
        message: str,
        src: str,
        start_pos: Position,
        end_pos: Position,
        type: ErrorType,
        help_text: str | None = None,
    ):
        self.message: str = message
        self.src: str = src
        self.start_pos: Position = start_pos
        self.end_pos: Position = end_pos
        self.type: ErrorType = type
        self.help_text = help_text

    def generate_error_text(self) -> str:
        res = f"{Colors.bright_red(f'{self.type} @ {str(self.start_pos)}')}\n"
        res += f"{Colors.bright_black('> ')}{Colors.red(self.message)}\n\n"
        res += self.generate_code_preview()

        if self.help_text:
            res += Colors.green(f"\n\n{Colors.bright_green('Hint:')} {self.help_text}")

        return f"{res}"

    def generate_code_preview(self) -> str:
        result: str = ""

        idx_start: int = max(self.src.rfind("\n", 0, self.start_pos.idx), 0)
        idx_end: int = self.src.find("\n", idx_start + 1)
        if idx_end < 0:
            idx_end = len(self.src)

        line_count: int = self.end_pos.ln - self.start_pos.ln + 1

        for i in range(line_count):
            line_number = f"{self.start_pos.ln + i + 1}  | "
            line: str = self.src[idx_start:idx_end]
            col_start: int = self.start_pos.col if i == 0 else 0
            col_end: int = self.end_pos.col if i == line_count - 1 else len(line) - 1

            line = f"{Colors.white(line[0:col_start])}{Colors.bright_white(line[col_start:col_end])}{Colors.bright_black(line[col_end:len(line)])}"

            result += Colors.bright_black(line_number) + line + "\n"
            result += f"{' ' * (len(line_number) - 4)}{Colors.bright_black('  | ')}{' ' * col_start}{Colors.bright_red('^') * (col_end - col_start)}"

            idx_start = idx_end
            idx_end = self.src.find("\n", idx_start + 1)
            if idx_end < 0:
                idx_end = len(self.src)

        return result.replace("\t", "")


class IllegalCharacterError(Error):
    def __init__(
        self,
        char,
        src: str,
        start_pos: Position,
        end_pos: Position,
        help_text: str | None = None,
    ):
        Error.__init__(
            self,
            f"Illegal Character {char}",
            src,
            start_pos,
            end_pos,
            "Lexer Error",
            help_text,
        )


class InvalidSyntaxError(Error):
    def __init__(
        self,
        src: str,
        details: str | None,
        start_pos: Position,
        end_pos: Position,
        help_text: str | None = None,
    ):
        Error.__init__(
            self,
            f"Invalid Syntax{': ' if details else ''}{details}",
            src,
            start_pos,
            end_pos,
            "Parser Error",
            help_text,
        )

