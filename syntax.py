# -------------------------------
# ANALISIS SINTACTICO
# -------------------------------

import lexer as lx
from lexer import tokens
import ply.yacc as yacc


args = []  # Argumentos temporales de las funciones
syntax_error = ""  # Pila de errores sintacticos
lines_of_error = []
tree = ()


def clear():
    global syntax_error
    global lines_of_error
    global tree
    syntax_error = ""
    lines_of_error = []
    tree = ()


def get_error():
    global syntax_error
    return syntax_error


def get_lines_error():
    global lines_of_error
    return lines_of_error


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
    tree = p[1]


def p_statements(p):
    """
    statements : function_definition statements
               | function_definition
    """
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]


def p_empty(p):
    """
    empty :
    """
    p[0] = None


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
                    | print
                    | for
                    | while
                    | break
                    | if_else
                    | move
                    | delay
    """
    p[0] = p[1]


def p_assignment(p):
    """
    assignment : LET ID ASSIGN expression SEMICOLON
               | LET ID ASSIGN expression empty
    """
    if p[5] == None:
        common_error("semicolon", p.lineno(1))
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


def p_expression_comparison(p):
    """
    expression : expression NOT_EQUAL expression 
               | expression GREATER_EQUAL_THAN expression
               | expression LESS_EQUAL_THAN expression
               | expression GREATER_THAN expression
               | expression LESS_THAN expression
               | expression EQUAL expression
    """
    p[0] = (p[2], p[1], p[3], p.lineno(1))


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
                   | ID L_PAREN arguments R_PAREN empty
    """
    global args
    args = []
    split_args(p[3])
    if p[5] == None:
        common_error("semicolon", p.lineno(1))
    p[0] = ("call", p[1], args, p.lineno(1))


def p_function_call(p):
    """
    function_call : ID L_PAREN arguments R_PAREN
    """
    global args
    args = []
    split_args(p[3])
    p[0] = ("call", p[1], args, p.lineno(1))


def p_return(p):
    """
    return : RETURN expression SEMICOLON
           | RETURN expression empty
           | RETURN SEMICOLON
           | RETURN empty
    """
    if len(p) == 4:
        p[0] = ("return", p[2], 0, p.lineno(1))
        if p[3] == None:
            common_error("semicolon", p.lineno(1))
    else:
        if p[2] == None:
            common_error("semicolon", p.lineno(1))
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


def p_print(p):
    """
    print : PRINT EXCL L_PAREN print_arguments R_PAREN SEMICOLON
          | PRINT EXCL L_PAREN print_arguments R_PAREN empty
    """
    global args
    args = []
    split_args(p[4])
    if p[6] == None:
        common_error("semicolon", p.lineno(1))
    p[0] = ("print", args, 0, p.lineno(1))


def p_print_arguments(p):
    """
    print_arguments : expression COMMA print_arguments
                    | text COMMA print_arguments
                    | expression
                    | text
    """
    if len(p) == 4:
        p[0] = [p[1]] + [p[3]]
    else:
        p[0] = p[1]


def p_text(p):
    """
    text : STRING
    """
    p[0] = ("text", p[1], 0, p.lineno(1))


def p_for(p):
    """
    for : FOR ID IN expression DOT_DOT ASSIGN expression L_CURLYBRACKET inner_statements R_CURLYBRACKET
        | FOR ID IN expression DOT_DOT expression L_CURLYBRACKET inner_statements R_CURLYBRACKET
    """
    if len(p) == 11:
        p[0] = ("for=", [p[2], p[4], p[7]], p[9], p.lineno(1))
    else:
        p[0] = ("for", [p[2], p[4], p[6]], p[8], p.lineno(1))


def p_while(p):
    """
    while : WHILE expression L_CURLYBRACKET inner_statements R_CURLYBRACKET
          | LOOP L_CURLYBRACKET inner_statements R_CURLYBRACKET
    """
    if len(p) == 6:
        p[0] = (p[1], p[2], p[4], p.lineno(1))
    else:
        p[0] = (p[1], 0, p[3], p.lineno(1))


def p_break(p):
    """
    break : BREAK SEMICOLON
          | BREAK empty
    """
    if p[2] == None:
        common_error("semicolon", p.lineno(1))
    p[0] = (p[1], 0, 0, p.lineno(1))


def p_if_else(p):
    """
    if_else : IF expression L_CURLYBRACKET inner_statements R_CURLYBRACKET ELSE L_CURLYBRACKET inner_statements R_CURLYBRACKET
            | IF expression L_CURLYBRACKET inner_statements R_CURLYBRACKET ELSE if_else
            | IF expression L_CURLYBRACKET inner_statements R_CURLYBRACKET
            
    """
    if len(p) == 10:
        p[0] = ("if-else", p[2], (p[4], p[8]), p.lineno(1))
    elif len(p) == 8:
        p[0] = ("if-else", p[2], (p[4], p[7]), p.lineno(1))
    else:
        p[0] = ("if", p[2], p[4], p.lineno(1))


def p_move(p):
    """
    move : MOVE L_PAREN L_SQUAREBRACKET finger_arguments R_SQUAREBRACKET COMMA expression R_PAREN SEMICOLON
         | MOVE L_PAREN L_SQUAREBRACKET finger_arguments R_SQUAREBRACKET COMMA expression R_PAREN empty
         | MOVE L_PAREN text COMMA expression R_PAREN SEMICOLON
         | MOVE L_PAREN text COMMA expression R_PAREN empty
    """
    global args
    args = []
    if len(p) == 10:
        if p[9] == None:
            common_error("semicolon", p.lineno(1))
        split_args(p[4])
        p[0] = ("Move", args, p[7], p.lineno(1))
    else:
        if p[7] == None:
            common_error("semicolon", p.lineno(1))
        p[0] = ("Move", [p[3]], p[5], p.lineno(1))


def p_finger_arguments(p):
    """
    finger_arguments : text COMMA finger_arguments
                     | text
    """
    if len(p) == 4:
        p[0] = [p[1]] + [p[3]]
    elif p[1] != None:
        p[0] = p[1]


def p_delay(p):
    """
    delay : DELAY L_PAREN expression COMMA text R_PAREN SEMICOLON
    """
    if p[7] == None:
        common_error("semicolon", p.lineno(1))
    p[0] = ("Delay", p[3], p[5], p.lineno(1))


# Reacomoda los argumentos en la lista
def split_args(a):
    global args
    if type(a) == list:
        for i in a:
            split_args(i)
    elif a != None:
        args.append(a)


# Manejo de errores sintacticos
def p_error(p):
    global syntax_error
    global lines_of_error

    if p:
        syntax_error += (
            "Línea "
            + str(p.lineno)
            + ": Error de sintaxis en, o antes de, el token: "
            + str(p.value)
            + "\n"
        )
        lines_of_error.append(p.lineno)
    else:
        syntax_error += "Error de sintaxis. Fin del archivo inesperado." + "\n"


# Errores comunes
def common_error(error_type, line):
    global syntax_error
    global lines_of_error

    if error_type == "semicolon":
        syntax_error += (
            "Línea " + str(line) + ": Punto y coma faltante al final de la sentencia.\n"
        )
        lines_of_error.append(line)


# Crea el parser
parser = yacc.yacc()

# Ejecuta el parser
def run_parser(text):
    global tree
    global parser

    parser.parse(text, tracking=True)

    return tree
