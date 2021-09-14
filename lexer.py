import ply.lex as lex

error_msg = ""
lines_of_error = []


def clear():
    global error_msg
    global lines_of_error
    error_msg = ""
    lexer.lineno = 1
    lines_of_error = []


def get_error():
    global error_msg
    return error_msg


def get_lines_error():
    global lines_of_error
    return lines_of_error


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
    "L_CURLYBRACKET",
    "R_CURLYBRACKET",
    "FUNCTION",
    "ARROW",
    "TYPE_INT",
    "TYPE_BOOL",
    "RETURN",
    "PRINT",
    "EXCL",
    "STRING",
]
"""
    "EQUAL",
    "NOT_EQUAL",
    "GREATER_EQUAL_THAN",
    "LESS_EQUAL_THAN",
    "GREATER_THAN",
    "LESS_THAN",
    "FOR",
    "IN",
    "DOT_DOT",
    "BEFORE",
    "UNTIL",
    "WHILE",
    "LOOP",
    "BREAK",
    "IF",
    "ELSE",
    "MOVE",
    "FINGER_P",
    "FINGER_I",
    "FINGER_M",
    "FINGER_A",
    "FINGER_Q",
    "ALL_FINGERS",
    "L_SQUAREBRACKET",
    "R_SQUAREBRACKET",
    "DELAY",
    "SECONDS",
    "MILISECONDS",
    "MINUTES"
"""


# Palabras reservadas
RESERVED = {
    "True": "TRUE",
    "False": "FALSE",
    "let": "LET",
    "Opera": "OPERA",
    "fn": "FUNCTION",
    "integer": "TYPE_INT",
    "boolean": "TYPE_BOOL",
    "return": "RETURN",
    "Println": "PRINT",
}


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
t_L_CURLYBRACKET = r"\{"
t_R_CURLYBRACKET = r"\}"
t_FUNCTION = r"fn"
t_ARROW = r"\->"
t_TYPE_INT = r"integer"
t_TYPE_BOOL = r"boolean"
t_RETURN = r"return"
t_PRINT = r"Println"
t_STRING = r"\"[^\"]*\""
t_EXCL = r"!"


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


def t_tab(t):
    r"\t"
    pass


t_ignore = r" "


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
    global lines_of_error
    error_msg += (
        "Caracter ilegal " + str(t.value[0]) + " en la línea " + str(t.lineno) + ".\n"
    )
    lines_of_error += [t.lineno]
    t.lexer.skip(1)


lexer = lex.lex()
