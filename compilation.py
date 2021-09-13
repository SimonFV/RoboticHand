import lexer as lx
import ply.yacc as yacc
import sys
import semantic as sm

from lexer import tokens


# -------------------------------
# ANALISIS SINTACTICO
# -------------------------------

# Variables globales
syntax_error = ""  # Pila de errores
tree = ()  # Arbol de parseo
args = []  # Argumentos temporales de las funciones
lines_with_errors = []  # Lista de lineas con los errores


# Reglas del parser
precedence = (
    ("right", "UMINUS"),
    ("left", "OR"),
    ("left", "AND"),
)


def p_start(p):
    """
    start : statements
          | empty
    """
    global tree
    global variables
    tree = p[1]
    variables = {}


def p_statements(p):
    """
    statements : statement statements
               | statement
    """
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]


def p_statement(p):
    """
    statement : assignment
              | function_definition
    """
    p[0] = p[1]


def p_empty(p):
    """
    empty :
    """
    p[0] = None


def p_assignment(p):
    """
    assignment : LET ID ASSIGN expression SEMICOLON
    """
    p[0] = (p[3], p[2], p[4], p.lineno(1))


def p_expression(p):
    """
    expression : OPERA L_PAREN PLUS COMMA expression COMMA expression R_PAREN
               | OPERA L_PAREN MINUS COMMA expression COMMA expression R_PAREN
               | OPERA L_PAREN MULT COMMA expression COMMA expression R_PAREN
               | OPERA L_PAREN DIV COMMA expression COMMA expression R_PAREN
               | OPERA L_PAREN POW COMMA expression COMMA expression R_PAREN
               | expression OR expression
               | expression AND expression
               | function_call
               | L_PAREN expression R_PAREN
               | ID
               | INT
               | TRUE
               | FALSE
    """
    if len(p) == 9:
        p[0] = (p[3], p[5], p[7], p.lineno(1))
    elif len(p) == 4 and p[1] != "(":
        p[0] = (p[2], p[1], p[3], p.lineno(1))
    elif len(p) == 4:
        p[0] = p[2]
    else:
        if p[1] == "True":
            p[0] = True
        elif p[1] == "False":
            p[0] = False
        else:
            p[0] = p[1]


def p_expression_uminus(p):
    "expression : MINUS INT %prec UMINUS"
    p[0] = -p[2]


def p_function_definition(p):
    """
    function_definition : FUNCTION ID L_PAREN id_arguments R_PAREN ARROW TYPE_INT L_CURLYBRACKET inner_statements R_CURLYBRACKET
                        | FUNCTION ID L_PAREN id_arguments R_PAREN ARROW TYPE_BOOL L_CURLYBRACKET inner_statements R_CURLYBRACKET
                        | FUNCTION ID L_PAREN id_arguments R_PAREN L_CURLYBRACKET inner_statements R_CURLYBRACKET
    """
    global args
    args = []
    split_args(p[4])
    if len(p) == 11:
        p[0] = (p[7], [p[2]] + args, p[9], p.lineno(1))
    else:
        p[0] = ("None", [p[2]] + args, p[7], p.lineno(1))


def p_procedure_call(p):
    """
    procedure_call : ID L_PAREN arguments R_PAREN SEMICOLON
    """
    global args
    args = []
    split_args(p[3])
    p[0] = ("call", p[1], args, p.lineno(1))


def p_function_call(p):
    """
    function_call : ID L_PAREN arguments R_PAREN
    """
    global args
    args = []
    split_args(p[3])
    p[0] = ("call", p[1], args, p.lineno(1))


def p_inner_statements(p):
    """
    inner_statements : inner_statement inner_statements
                     | inner_statement
    """
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]


def p_inner_statement(p):
    """
    inner_statement : assignment
                    | return
                    | procedure_call
    """
    p[0] = p[1]


def p_return(p):
    """
    return : RETURN expression SEMICOLON
           | RETURN empty SEMICOLON
    """
    if len(p) == 4:
        p[0] = ("return", p[2], 0, p.lineno(1))
    else:
        p[0] = ("return", None, 0, p.lineno(1))


def p_arguments(p):
    """
    arguments : expression COMMA arguments
              | expression
              | empty
    """
    if len(p) == 4:
        p[0] = [p[1]] + [p[3]]
    elif p[1] != None:
        p[0] = p[1]


def p_id_arguments(p):
    """
    id_arguments : ID COMMA id_arguments
                 | ID
                 | empty
    """
    if len(p) == 4:
        p[0] = [p[1]] + [p[3]]
    elif p[1] != None:
        p[0] = p[1]


def p_error(p):
    global syntax_error
    if p:
        syntax_error += (
            "Línea "
            + str(p.lineno)
            + ": Error de sintaxis en [ "
            + str(p.value)
            + " ]\n"
        )
        lines_with_errors.append(p.lineno)
    else:
        syntax_error += "Error de sintaxis. EOF inesperado." + "\n"


# Reacomoda los argumentos en la lista
def split_args(a):
    global args
    if type(a) == list:
        for i in a:
            split_args(i)
    elif a != None:
        args.append(a)


# Crea el parser
parser = yacc.yacc()


# Inicia la compilación del código
def compiling(app):
    global tree
    global syntax_error
    global lines_with_errors
    syntax_error = ""
    lines_with_errors = []
    app.log("Compilando...\n", type_msg="info")
    lx.clear()
    sm.clear()

    # Analisis lexico
    lx.lexer.input(app.get_text())
    while True:
        tok = lx.lexer.token()
        if not tok:
            break
        # else:
        # app.log("Tokens encontrados:\n", type_msg="info")
        # app.log(str(tok) + "\n", type_msg="success")
    if lx.get_error() != "":  # Detiene la compilacion: ERROR LEXICO
        highlight_errors(app)
        app.log(lx.get_error() + "\n", type_msg="error")
        return
    lx.clear()
    app.log("No se encontraron errores léxicos!\n", type_msg="success")

    # Analisis sintactico
    parser.parse(app.get_text(), tracking=True)
    if syntax_error != "":  # Detiene la compilacion: ERROR SINTACTICO
        app.log(syntax_error, type_msg="error")
        highlight_errors(app)
        return
    app.log("No se encontraron errores sintácticos!\n", type_msg="success")

    # Analisis semantico
    # print(tree)
    sm.check_semantics(tree)
    if sm.get_error() != "":  # Detiene la compilacion: ERROR SEMANTICO
        app.log(sm.get_error(), type_msg="error")
        lines_with_errors += sm.get_lines_error()
        highlight_errors(app)
        return
    app.log("No se encontraron errores semánticos!\n", type_msg="success")

    app.log("\nCompilación finalizada con éxito!!\n\n", type_msg="success")


# Inicia la compilación y ejecución del código
def compiling_running(app):
    compiling(app)
    app.log("Ejecutando!!\n", type_msg="success")


def highlight_errors(app):
    global lines_with_errors
    for i in lines_with_errors:
        app.highlight(i)
