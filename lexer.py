import ply.lex as lex

error_msg = ""


def clear():
    global error_msg
    error_msg = ""
    lexer.lineno = 1


def get_error():
    global error_msg
    return error_msg


# Lista de Tokens
tokens = [
    "ID",
    "INT",
    "TRUE",
    "FALSE",
    "SEMICOLON",
    "LET",
    "ASSIGN",
    "L_PAREN",
    "R_PAREN",
    "PLUS",
    "MINUS",
    "MULT",
    "DIV",
    "POW",
    "OPERA",
    "COMMA",
    "AND",
    "OR",
]
"""
    "L_CURLYBRACKET",
    "R_CURLYBRACKET",
    "L_SQUAREBRACKET",
    "R_SQUAREBRACKET",
    "EQUAL",
    "NOT_EQUAL",
    "GREATER_EQUAL_THAN",
    "LESS_EQUAL_THAN",
    "GREATER_THAN",
    "LESS_THAN",
    "DOT",
    "FOR",
    "RANGE",
    "IN",
    "BEFORE",
    "UNTIL",
    "WHILE",
    "LOOP",
    "BREAK",
    "IF",
    "ELSE",
    "FUNCTION",
    "ARROW",
    "TYPE_INT",
    "TYPE_BOOL",
    "RETURN",
    "PRINT",
    "MOVE",
    "FINGER_P",
    "FINGER_I",
    "FINGER_M",
    "FINGER_A",
    "FINGER_Q",
    "ALL_FINGERS",
    "DELAY",
    "SECONDS",
    "MILISECONDS",
    "MINUTES","""

# Palabras reservadas
RESERVED = {"True": "TRUE", "False": "FALSE", "let": "LET", "Opera": "OPERA"}


# Expresiones regulares

t_SEMICOLON = r";"
t_LET = r"let"
t_ASSIGN = r"="
t_L_PAREN = r"\("
t_R_PAREN = r"\)"
t_PLUS = r"\+"
t_MINUS = r"\-"
t_MULT = r"\*"
t_DIV = r"/"
t_POW = r"\*\*"
OPERA = r"Opera"
t_COMMA = r","
t_AND = r"&"
t_OR = r"\|"


def t_ID(t):
    r"[a-zA-Z_#?][a-zA-Z_#?0-9]{2,14}"
    t.type = RESERVED.get(t.value, "ID")
    return t


def t_comment(t):
    r"[ ]*@[^\n]*"
    pass


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


t_ignore = r" \t\n"


def t_INT(t):
    r"\d+"
    global error_msg
    try:
        t.value = int(t.value)
    except ValueError:
        error_msg += "Valor del entero es muy grande: " + str(t.value)
        t.value = 0
    return t


def t_TRUE(t):
    r"True"
    t.value = True
    return t


def t_FALSE(t):
    r"False"
    t.value = False
    return t


def t_error(t):
    global error_msg
    error_msg += (
        "Caracter ilegal " + str(t.value[0]) + " en la línea " + str(t.lineno) + ".\n"
    )
    t.lexer.skip(1)


lexer = lex.lex()