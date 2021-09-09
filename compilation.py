import lexer as lx
import ply.yacc as yacc
import sys

from lexer import tokens

syntax_error = ""
semantic_error = ""
line_error = 1

# Reglas del parser

precedence = (
    ("left", "OR"),
    ("left", "AND"),
)

# Arbol
tree = ()

# Tabla de valores
variables = {}  # {nombre: valor}


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
    statement : assign
    """
    p[0] = p[1]


def p_empty(p):
    """
    empty :
    """
    p[0] = None


def p_assign(p):
    """
    assign : LET ID ASSIGN expression SEMICOLON
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
    print(p[0])


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
    else:
        syntax_error += "Error de sintaxis. EOF inesperado." + "\n"


parser = yacc.yacc()


# Inicia la compilación del código
def compiling(app):
    global tree
    global semantic_error
    global syntax_error
    semantic_error = ""
    syntax_error = ""
    app.log("Compilando...\n", type_msg="info")
    lx.clear()

    # Analisis lexico
    lx.lexer.input(app.get_text())
    while True:
        tok = lx.lexer.token()
        if not tok:
            break
        else:
            # app.log("Tokens encontrados:\n", type_msg="info")
            app.log(str(tok) + "\n", type_msg="success")
    if lx.get_error() != "":  # Detiene la compilacion: ERROR LEXICO
        app.log(lx.get_error() + "\n", type_msg="error")
        return
    lx.clear()
    app.log("No se encontraron errores léxicos!\n", type_msg="success")

    # Analisis sintactico
    parser.parse(app.get_text())
    if syntax_error != "":  # Detiene la compilacion: ERROR SINTACTICO
        app.log(syntax_error, type_msg="error")
        return
    app.log("No se encontraron errores sintácticos!\n", type_msg="success")

    # Analisis semantico
    # print(tree)
    test(tree)
    # print(variables)
    if semantic_error != "":  # Detiene la compilacion: ERROR SEMANTICO
        app.log(semantic_error, type_msg="error")
        return
    app.log("No se encontraron errores semánticos!\n", type_msg="success")

    app.log("\nCompilación finalizada con éxito!!\n\n", type_msg="success")


# Inicia la compilación y ejecución del código
def compiling_running(app):
    compiling(app)
    app.log("Ejecutando!!\n", type_msg="success")


# ---------------------------------------------
# ANALISIS SEMANTICO
# ---------------------------------------------

# Prueba el arbol en busca de errores semanticos
def test(p):
    global line_error
    global variables
    global semantic_error
    if type(p) == tuple:
        if len(p) == 4:
            line_error = p[3]
        # Asignacion de variables
        if p[0] == "=":
            var = test(p[2])
            if var == None:
                return
            if (p[1] in variables) and type(variables[p[1]]) != type(var):
                semantic_error += (
                    "Línea "
                    + str(p[3])
                    + ": La variable "
                    + str(p[1])
                    + " está definida con otro tipo."
                    + "\n"
                )
            else:
                variables[p[1]] = var

        # Operaciones matematicas
        elif p[0] == "+":
            if type(test(p[1])) == int and type(test(p[2])) == int:
                return test(p[1]) + test(p[2])
            semantic_error += (
                "Línea "
                + str(line_error)
                + ": Ambos operandos deben ser enteros."
                + "\n"
            )
            return None
        elif p[0] == "-":
            if type(test(p[1])) == int and type(test(p[2])) == int:
                return test(p[1]) - test(p[2])
            semantic_error += (
                "Línea "
                + str(line_error)
                + ": Ambos operandos deben ser enteros."
                + "\n"
            )
            return None
        elif p[0] == "*":
            if type(test(p[1])) == int and type(test(p[2])) == int:
                return test(p[1]) * test(p[2])
            semantic_error += (
                "Línea "
                + str(line_error)
                + ": Ambos operandos deben ser enteros."
                + "\n"
            )
            return None
        elif p[0] == "/":
            if type(test(p[1])) == int and type(test(p[2])) == int:
                return int(test(p[1]) / test(p[2]))
            semantic_error += (
                "Línea "
                + str(line_error)
                + ": Ambos operandos deben ser enteros."
                + "\n"
            )
            return None
        elif p[0] == "**":
            if type(test(p[1])) == int and type(test(p[2])) == int:
                return test(p[1]) ** test(p[2])
            semantic_error += (
                "Línea "
                + str(line_error)
                + ": Ambos operandos deben ser enteros."
                + "\n"
            )
            return None

        # Operaciones logicas
        elif p[0] == "|":
            if type(test(p[1])) == bool and type(test(p[2])) == bool:
                return test(p[1]) or test(p[2])
            semantic_error += (
                "Línea "
                + str(line_error)
                + ": Ambos operandos deben ser booleanos."
                + "\n"
            )
            return None
        elif p[0] == "&":
            if type(test(p[1])) == bool and type(test(p[2])) == bool:
                return test(p[1]) and test(p[2])
            semantic_error += (
                "Línea "
                + str(line_error)
                + ": Ambos operandos deben ser booleanos."
                + "\n"
            )
            return None

        # Recorre el resto del arbol
        else:
            for i in range(len(p)):
                test(p[i])

    # Si no es una tupla y es una variable, prueba si existe
    elif type(p) != bool and type(p) != int:
        if is_var_defined(p):
            return variables[p]
        else:
            return None

    # Es una constante
    else:
        return p


def is_var_defined(var):
    global variables
    global line_error
    global semantic_error
    try:
        var = variables[var]
    except LookupError:
        semantic_error += (
            "Línea " + str(line_error) + ": Identificador no definido: " + var + "\n"
        )
        return False
    return True
