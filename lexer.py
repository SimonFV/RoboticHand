# ---------------------------------------------
# ANALISIS LEXICO
# ---------------------------------------------


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
    "WRONG_ID_MIN",
    "WRONG_ID_MAX",
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
    "EQUAL",
    "NOT_EQUAL",
    "GREATER_EQUAL_THAN",
    "LESS_EQUAL_THAN",
    "GREATER_THAN",
    "LESS_THAN",
    "FOR",
    "IN",
    "DOT_DOT",
    "WHILE",
    "LOOP",
    "BREAK",
    "IF",
    "ELSE",
    "MOVE",
    "L_SQUAREBRACKET",
    "R_SQUAREBRACKET",
    "DELAY",
]


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
    "println": "PRINT",
    "for": "FOR",
    "in": "IN",
    "while": "WHILE",
    "loop": "LOOP",
    "break": "BREAK",
    "if": "IF",
    "else": "ELSE",
    "Move": "MOVE",
    "Delay": "DELAY",
}


# Expresiones regulares

t_SEMICOLON = r";"
t_LET = r"let"
t_NOT_EQUAL = r"<>"
t_GREATER_EQUAL_THAN = r">="
t_LESS_EQUAL_THAN = r"<="
t_GREATER_THAN = r">"
t_LESS_THAN = r"<"
t_EQUAL = r"=="
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
t_PRINT = r"println"
t_STRING = r"\"[^\"]*\""
t_EXCL = r"!"
t_FOR = r"for"
t_IN = r"in"
t_DOT_DOT = r"\.\."
t_WHILE = r"while"
t_LOOP = r"loop"
t_BREAK = r"break"
t_IF = r"if"
t_ELSE = r"else"
t_MOVE = r"Move"
t_L_SQUAREBRACKET = r"\["
t_R_SQUAREBRACKET = r"\]"
t_DELAY = r"Delay"


def t_WRONG_ID_MAX(t):
    r"[a-zA-Z_#?][a-zA-Z_#?0-9]{15,}"
    global error_msg
    t.type = RESERVED.get(t.value, "WRONG_ID_MAX")
    if t.type == "WRONG_ID_MAX":
        error_msg += (
            "Línea "
            + str(t.lineno)
            + ": Identificador ilegal "
            + str(t.value)
            + ". Máximo 15 caracteres.\n"
        )
    return t


def t_ID(t):
    r"[a-zA-Z_#?][a-zA-Z_#?0-9]{2,14}"
    t.type = RESERVED.get(t.value, "ID")
    return t


def t_WRONG_ID_MIN(t):
    r"[a-zA-Z_#?][a-zA-Z_#?0-9]{1}"
    global error_msg
    t.type = RESERVED.get(t.value, "WRONG_ID_MIN")
    if t.type == "WRONG_ID_MIN":
        error_msg += (
            "Línea "
            + str(t.lineno)
            + ": Identificador ilegal "
            + str(t.value)
            + ". Mínimo 3 caracteres.\n"
        )
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
