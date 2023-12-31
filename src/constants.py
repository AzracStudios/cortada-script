## ARITHNETIC ##
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_FLRDIV = "FLRDIV"
TT_POW = "POW"
TT_MOD = "MOD"

## LOGIC ##
TT_LT = "LT"
TT_GT = "GT"
TT_LTE = "LTE"
TT_GTE = "GTE"
TT_EQL = "EQL"
TT_NEQL = "NEQL"
TT_AT = "AT"

## ASSIGN ##
TT_ASSIGN = "ASSIGN"
TT_INC = "INC"
TT_DEC = "DEC"
TT_SUMASSIGN = "SUMASSIGN"
TT_SUBASSIGN = "SUBASSIGN"
TT_MULASSIGN = "MULASSIGN"
TT_DIVASSIGN = "DIVASSIGN"
TT_POWASSIGN = "POWASSIGN"
TT_MODASSIGN = "MODASSIGN"

## BRAC ##
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_LBRACK = "LBRACK"
TT_RBRACK = "RBRACK"
TT_LBRACE = "LBRACE"
TT_RBRACE = "RBRACE"

## MISC ##
TT_SPACE = "SPACE"
TT_COMMA = "COMMA"
TT_ARROW = "ARROW"
TT_NL = "NL"
TT_EOF = "EOF"

## CONSTS ##
NUM_STR = ".0123456789"
ALPH_STR = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

## DATA ##
TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_STRING = "STRING"
TT_FMT_STRING = "FMT_STRING"
TT_KWRD = "KWRD"
TT_IDENT = "IDENT"

## KWRD ##
KWRDS = [
    "var",
    "fn",
    #####
    "if",
    "elif",
    "else",
    "then",
    "while",
    "do",
    #####
    "and",
    "or",
    "in",
    "not",
    "true",
    "false",
    "nil",
    #####
    "return",
    "continue",
    "break",
    "end",
]
