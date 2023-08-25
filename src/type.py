from typing import Literal, TypeAlias, Any

TokenType: TypeAlias = (
    Literal[
        "PLUS",
        "MINUS",
        "MUL",
        "DIV",
        "FLRDIV",
        "POW",
        "MOD",
        "LT",
        "GT",
        "LTE",
        "GTE",
        "EQL",
        "NEQL",
        "COL",
        "COMMA",
        "ARROW",
        "ASSIGN",
        "INC",
        "DEC",
        "SUMASSIGN",
        "SUBASSIGN",
        "MULASSIGN",
        "DIVASSIGN",
        "FLRDIVASSIGN",
        "POWASSIGN",
        "MODASSIGN",
        "LPAREN",
        "RPAREN",
        "LBRACK",
        "RBRACK",
        "LBRACE",
        "RBRACE",
        "INT",
        "FLOAT",
        "STRING",
        "FMT_STRING",
        "KWRD",
        "IDENT",
        "EOF",
    ] | None
)

TokenValue: TypeAlias = int | float | str | list[tuple[(Any | list), str]] | None 

ErrorType: TypeAlias = Literal["Lexer Error", "Parser Error", "Runtime Error"]