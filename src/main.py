from lexer import Lexer
from tok import Token
from error import Error
from _parser import Parser
from parser_nodes import Node
from typing import Any


def run(src: str, debug: bool = False) -> tuple[Node | None, Error | None]:
    lexer = Lexer("shell", src)
    toks: list[Token] | Error = lexer.tokenize()

    if isinstance(toks, Error):
        return None, toks

    else:
        if debug:
            print("## TOKENS ##\n[", end="")
            for i, tok in enumerate(toks):
                print(tok, end=", " if i < len(toks) - 1 else "")
            print("]\n")

        parser = Parser(toks, src)
        res = parser.parse()
        return res.node, res.error
