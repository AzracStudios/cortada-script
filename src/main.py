from lexer import Lexer
from tok import Token
from error import Error
from _parser import Parser
from parser_nodes import Node
from interpreter import *
import os
import platform

global_symbol_table = SymbolTable()

global_symbol_table.set("print", BuiltinFunction.print)
global_symbol_table.set("print_eol", BuiltinFunction.print_eol)
global_symbol_table.set("hello_world", BuiltinFunction.hello_world)
global_symbol_table.set("input", BuiltinFunction.input)
global_symbol_table.set("clear", BuiltinFunction.clear)

global_symbol_table.set("to_int", BuiltinFunction.to_int)
global_symbol_table.set("to_float", BuiltinFunction.to_float)
global_symbol_table.set("to_string", BuiltinFunction.to_string)
global_symbol_table.set("to_bool", BuiltinFunction.to_bool)

global_symbol_table.set("type", BuiltinFunction.type)


def run(src, debug=False, file_name="<stdin>"):
    # ENABLE ANSI SUPPORT ON WINDOWS
    if platform.system() == "Windows":
        os.system("color")

    if src.strip() == "":
        return None, None
    lexer = Lexer(file_name, src)
    toks = lexer.tokenize()

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

        context = Context("<global>")
        context.symbol_table = global_symbol_table
        res = Interpreter.visit(res.node, context)

        if debug:
            print("## RESULT ##")

        return res.value, res.error
