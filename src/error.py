from position import Position
from color import Colors


class Error:
    def __init__(
        self,
        message,
        src,
        start_pos,
        end_pos,
        type,
        help_text = None,
    ):
        self.message = message
        self.src = src
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.type = type
        self.help_text = help_text

    def generate_error_text(self):
        res = f"{Colors.bright_red(f'{self.type} @ {str(self.start_pos)}')}\n"
        res += f"{Colors.bright_black('> ')}{Colors.red(self.message)}\n\n"
        res += self.generate_code_preview()

        if self.help_text:
            res += Colors.green(f"\n\n{Colors.bright_green('Hint:')} {Colors.green(self.help_text)}")

        return f"{res}"

    def generate_code_preview(self):
        result = ""

        idx_start = max(self.src.rfind("\n", 0, self.start_pos.idx), 0)
        idx_end = self.src.find("\n", idx_start + 1)
        if idx_end < 0:
            idx_end = len(self.src)

        line_count = self.end_pos.ln - self.start_pos.ln + 1
        if self.end_pos.ln > 1:
            line_count += 1
            

        for i in range(line_count):
            sp = len(str(self.start_pos.ln + line_count))
            line_number = f"{self.start_pos.ln + i + 1}{' ' * (sp - len(str(self.start_pos.ln + i + 1)) + 1)}| "
            line = self.src[idx_start:idx_end].replace("\n", "")
            col_start = self.start_pos.col if i == 0 else 0
            col_end = self.end_pos.col if i == line_count - 1 else len(line) - 1

            if self.end_pos.ln < self.start_pos.ln + i:
                line = f"{Colors.bright_black(line)}"
                result += Colors.bright_black(line_number) + line + "\n"
            else:
                line = f"{Colors.white(line[0:col_start])}{Colors.bright_white(line[col_start:col_end+1])}{Colors.bright_black(line[col_end+1:len(line)])}"
                result += Colors.bright_black(line_number) + line + "\n"
                result += f"{' ' * (len(line_number) - 4)}{Colors.bright_black('  | ')}{' ' * col_start}{Colors.bright_red('^') * (col_end - col_start+1)}\n"

            idx_start = idx_end
            idx_end = self.src.find("\n", idx_start + 1)
            if idx_end < 0:
                idx_end = len(self.src)

        return result.replace("\t", "")


class IllegalCharacter(Error):
    def __init__(
        self,
        char,
        start_pos,
        end_pos,
        help_text = None,
    ):
        Error.__init__(
            self,
            f"Illegal Character {char}",
            start_pos.file_src,
            start_pos,
            end_pos,
            "Lexer Error",
            help_text,
        )


class UnterminatedString(Error):
    def __init__(
        self,
        start_pos,
        end_pos,
        term_char,
    ):
        char_text = '\'"\''
        if term_char == "'":
            char_text = "\"'\""
        elif term_char == "`":
            char_text = "'`'"
        
        Error.__init__(
            self,
            f"Unterminated String",
            start_pos.file_src,
            start_pos,
            end_pos,
            "Lexer Error",
            f'Try adding a {char_text} at the end of the line',
        )


class InvalidSyntax(Error):
    def __init__(
        self,
        details,
        start_pos,
        end_pos,
        help_text = None,
    ):
        Error.__init__(
            self,
            f"Invalid Syntax{': ' if details else ''}{details}",
            start_pos.file_src,
            start_pos,
            end_pos,
            "Parser Error",
            help_text,
        )


class RTError(Error):
    def __init__(
        self,
        start_pos,
        end_pos,
        details,
        context,
        help_text = None,
    ):
        self.context = context
        Error.__init__(
            self,
            details,
            start_pos.file_src,
            start_pos,
            end_pos,
            "Runtime Error",
            help_text,
        )

    def generate_error_text(self):
        res = f"{self.generate_traceback()}\n"
        res += f"{Colors.bright_red(f'{self.type} @ {str(self.start_pos)}')}\n"
        res += f"{Colors.bright_black('> ')}{Colors.red(self.message)}\n\n"
        res += self.generate_code_preview()

        if self.help_text:
            res += Colors.green(f"\n\n{Colors.bright_green('Hint:')} {self.help_text}")

        return f"{res}"

    def generate_traceback(self):
        result = ""
        pos = self.start_pos
        ctx = self.context

        while ctx:
            result = f"File {Colors.bright_white(pos.file_name)}, line {pos.ln + 1}, in {Colors.bright_white(ctx.display_name)}\n{result}"  # type:ignore
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return f"{Colors.bright_red('Traceback')} {Colors.red('(most recent call last)')}:\n{result}"


### RUNTIME ERRORS ###
class ReferenceError(RTError):
    def __init__(
        self,
        details,
        start_pos,
        end_pos,
        context,
        help_text = None,
    ):
        RTError.__init__(
            self,
            start_pos,
            end_pos,
            f"ReferenceError: {details}",
            context,
            help_text,
        )

class ValueError(RTError):
    def __init__(self, details, start_pos, end_pos, context):
        RTError.__init__(
            self,
            start_pos,
            end_pos, 
            f"ValueError: {details}",
            context,
        )


class TypeError(RTError):
    def __init__(self, details, start_pos, end_pos, context):
        RTError.__init__(
            self,
            start_pos,
            end_pos,
            f"TypeError: {details}",
            context,
        )

class IndexOutOfBoundsError(RTError):
    def __init__(self, details, start_pos, end_pos, context):
        RTError.__init__(
            self,
            start_pos,
            end_pos,
            f"IndexOutOfBounds: {details}",
            context,
        )
