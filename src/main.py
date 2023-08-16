from lexer import Lexer
from tok import Token
from error import Error
from _parser import Parser
from parser_nodes import Node
from interpreter import Interpreter
from rtval import Value
from symboltable import SymbolTable
from context import Context

import os
import platform

global_symbol_table = SymbolTable()
global_symbol_table.set("nil", 0)


def run(src: str, debug: bool = False) -> tuple[Value | None, Error | None]:
    # ENABLE ANSI SUPPORT ON WINDOWS
    if platform.system() == "Windows":
        os.system("color")

    lexer = Lexer("<stdin>", src)
    toks: list[Token] | Error = lexer.tokenize()

    if isinstance(toks, Error):
        return None, toks

    else:
        if debug:
            print("## TOKENS ##\n[", end="")
            for i, tok in enumerate(toks):
                print(tok, end=", " if i < len(toks) - 1 else "")
            print("]\n")

        parser = Parser(toks)
        res = parser.parse()
        if res.error or not res.node:
            return None, res.error

        if debug:
            print("## ABSTRACT SYNTAX TREE ##")
            print(f"{res.node}\n")

        interpreter = Interpreter()
        context = Context("<shell>")
        context.symbol_table = global_symbol_table
        res = interpreter.visit(res.node, context)

        if debug:
            print("## RESULT ##")
        return res.value, res.error
