import ply.lex as lex
import ply.yacc as yacc
import sys

error_msg = ""

# ----------------------------------------------------------
# LEXER
# ----------------------------------------------------------

# Lista de Tokens
tokens = ["ID", "INT", "TRUE", "FALSE"]  # check  # check  # check  # check
""""AND",
    "OR",
    "L_PAREN",
    "R_PAREN",
    "L_CURLYBRACKET",
    "R_CURLYBRACKET",
    "L_SQUAREBRACKET",
    "R_SQUAREBRACKET",
    "PLUS",
    "MINUS",
    "MULT",
    "DIV",
    "POW",
    "OPERA",
    "EQUAL",
    "ASSIGN",
    "NOT_EQUAL",
    "GREATER_EQUAL_THAN",
    "LESS_EQUAL_THAN",
    "GREATER_THAN",
    "LESS_THAN",
    "LET",
    "COMMA",
    "DOT",
    "SEMICOLON",
    "COMMENT",
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
    "FINGER_P",  # PULGAR
    "FINGER_I",  # INDICE
    "FINGER_M",  # MEDIO
    "FINGER_A",  # ANULAR
    "FINGER_Q",  # MEÑIQUE
    "ALL_FINGERS",
    "DELAY",
    "SECONDS",
    "MILISECONDS",
    "MINUTES","""


# Expresiones regulares

t_ID = r"[a-zA-Z_#?][a-zA-Z_#?0-9]{2,14}"


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


t_ignore = r" \t"


def t_INT(t):
    r"\d+"
    t.value = int(t.value)
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

# Inicia la compilación del código
def compiling(app):
    global error_msg
    error_msg = ""
    lexer.lineno = 1
    app.log("Compilando!!\n", type_msg="info")
    app.log("Tokens encontrados:\n", type_msg="info")

    # Solicita y realiza el analisis lexico al codigo
    lexer.input(app.get_text())
    while True:
        tok = lexer.token()
        if not tok:
            print(error_msg)
            break
        else:
            print(tok)


# Inicia la compilación y ejecución del código
def compiling_running(app):
    compiling(app)
    app.log("Ejecutando!!\n", type_msg="success")
