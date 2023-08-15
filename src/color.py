# COLORS
# ? REF: https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html

class Colors:
    # Generates code for standard ANSI color codes along with a basic test
    # PS: I am too lazy to write the functions out myself :)

    @staticmethod
    def generate_code():
        colors: list[str] = [
            "black",
            "red",
            "green",
            "yellow",
            "blue",
            "magenta",
            "cyan",
            "white",
        ]

        code: str = ""

        for i in range(len(colors)):
            code += f"""
    @staticmethod
    def {colors[i]}(text: str) -> str:
        return f\'\\u001b[{30 + i}m{'{'}text{'}'}\\u001b[0m\'

    @staticmethod
    def bright_{colors[i]}(text: str) -> str:
        return f\'\\u001b[{30 + i};1m{'{'}text{'}'}\\u001b[0m\'
"""

    @staticmethod
    def black(text: str) -> str:
        return f"\u001b[30m{text}\u001b[0m"

    @staticmethod
    def bright_black(text: str) -> str:
        return f"\u001b[30;1m{text}\u001b[0m"

    @staticmethod
    def red(text: str) -> str:
        return f"\u001b[31m{text}\u001b[0m"

    @staticmethod
    def bright_red(text: str) -> str:
        return f"\u001b[31;1m{text}\u001b[0m"

    @staticmethod
    def green(text: str) -> str:
        return f"\u001b[32m{text}\u001b[0m"

    @staticmethod
    def bright_green(text: str) -> str:
        return f"\u001b[32;1m{text}\u001b[0m"

    @staticmethod
    def yellow(text: str) -> str:
        return f"\u001b[33m{text}\u001b[0m"

    @staticmethod
    def bright_yellow(text: str) -> str:
        return f"\u001b[33;1m{text}\u001b[0m"

    @staticmethod
    def blue(text: str) -> str:
        return f"\u001b[34m{text}\u001b[0m"

    @staticmethod
    def bright_blue(text: str) -> str:
        return f"\u001b[34;1m{text}\u001b[0m"

    @staticmethod
    def magenta(text: str) -> str:
        return f"\u001b[35m{text}\u001b[0m"

    @staticmethod
    def bright_magenta(text: str) -> str:
        return f"\u001b[35;1m{text}\u001b[0m"

    @staticmethod
    def cyan(text: str) -> str:
        return f"\u001b[36m{text}\u001b[0m"

    @staticmethod
    def bright_cyan(text: str) -> str:
        return f"\u001b[36;1m{text}\u001b[0m"

    @staticmethod
    def white(text: str) -> str:
        return f"\u001b[37m{text}\u001b[0m"

    @staticmethod
    def bright_white(text: str) -> str:
        return f"\u001b[37;1m{text}\u001b[0m"

    @staticmethod
    def test_palette() -> None:
        print(
            "\n",
            Colors.black("███"),
            Colors.red("███"),
            Colors.green("███"),
            Colors.yellow("███"),
            Colors.blue("███"),
            Colors.magenta("███"),
            Colors.cyan("███"),
            Colors.white("███"),
            "\n",
            Colors.bright_black("███"),
            Colors.bright_red("███"),
            Colors.bright_green("███"),
            Colors.bright_yellow("███"),
            Colors.bright_blue("███"),
            Colors.bright_magenta("███"),
            Colors.bright_cyan("███"),
            Colors.bright_white("███"),
            "\n",
            sep=""
        )