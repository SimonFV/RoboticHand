import lexer as lx
import ply.yacc as yacc
import sys

from lexer import tokens

syntax_error = ""
semantic_error = ""
line_of_error = 1

# Reglas del parser

precedence = (
    ("left", "PLUS", "MINUS"),
    ("left", "MULT", "DIV"),
    ("left", "OR"),
    ("left", "AND"),
)

# Tabla de valores
variables = {}


def p_start(p):
    """
    start : expressions
          | empty
    """
    print(p[1])
    run(p[1])
    print(variables)


def p_expressions(p):
    """
    expressions : expression expressions
                | expression
    """
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]


def p_expression(p):
    """
    expression : assign
    """
    p[0] = p[1]


def p_empty(p):
    """
    empty :
    """
    p[0] = None


def p_assign(p):
    """
    assign : LET ID ASSIGN int_expression SEMICOLON
           | LET ID ASSIGN bool_expression SEMICOLON
    """
    p[0] = (p[3], p[2], p[4])


def p_int_expression(p):
    """
    int_expression : OPERA L_PAREN PLUS COMMA int_expression COMMA int_expression R_PAREN
                   | OPERA L_PAREN MINUS COMMA int_expression COMMA int_expression R_PAREN
                   | OPERA L_PAREN MULT COMMA int_expression COMMA int_expression R_PAREN
                   | OPERA L_PAREN DIV COMMA int_expression COMMA int_expression R_PAREN
                   | OPERA L_PAREN POW COMMA int_expression COMMA int_expression R_PAREN
                   | L_PAREN int_expression R_PAREN
                   | ID
                   | INT
    """
    if len(p) == 8:
        p[0] = (p[3], p[5], p[7])
    elif len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_bool_expression(p):
    """
    bool_expression : bool_expression OR bool_expression
                    | bool_expression AND bool_expression
                    | L_PAREN bool_expression R_PAREN
                    | ID
                    | TRUE
                    | FALSE
    """
    if len(p) == 4 and p[1] != "(":
        p[0] = (p[2], p[1], p[3])
    elif len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_error(p):
    global syntax_error
    if p:
        syntax_error += (
            "Error de sintaxis en [ "
            + str(p.value)
            + " ], linea: "
            + str(p.lineno)
            + "\n"
        )
    else:
        syntax_error += "Error de sintaxis." + "\n"


parser = yacc.yacc()


# Inicia la compilación del código
def compiling(app):
    global semantic_error
    global syntax_error
    semantic_error = ""
    syntax_error = ""
    app.log("Compilando...\n", type_msg="info")
    app.log("Tokens encontrados:\n", type_msg="info")
    lx.clear()

    # Solicita y realiza el analisis lexico al codigo
    lx.lexer.input(app.get_text())
    while True:
        tok = lx.lexer.token()
        if not tok:
            app.log(lx.get_error() + "\n", type_msg="error")
            break
        else:
            app.log(str(tok) + "\n", type_msg="success")
    if lx.get_error() != "":  # Detiene la compilacion
        return
    lx.clear()

    # Analisis sintactico
    parser.parse(app.get_text())
    if syntax_error != "":  # Detiene la compilacion
        app.log(syntax_error, type_msg="error")
        return

    app.log(semantic_error, type_msg="error")


# Inicia la compilación y ejecución del código
def compiling_running(app):
    compiling(app)
    app.log("Ejecutando!!\n", type_msg="success")


def run(p):
    global variables
    global semantic_error
    if type(p) == tuple:
        if p[0] == "=":  # Asignacion de variables
            var = run(p[2])
            if (p[1] in variables) and type(variables[p[1]]) != type(var):
                semantic_error += (
                    "La variable " + str(p[1]) + " ya se definio con otro tipo."
                )
            else:
                variables[p[1]] = var

        else:  # Recorre el resto del arbol
            for i in range(len(p)):
                run(p[i])
    else:
        return p
