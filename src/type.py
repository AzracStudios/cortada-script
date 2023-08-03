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
        "ASSIGN",
        "INC",
        "DEC",
        "SUMASSIGN",
        "MINASSIGN",
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
        "KWRD",
        "IDENT"
    ] | None
)

TokenValue: TypeAlias = int | float | str | None 