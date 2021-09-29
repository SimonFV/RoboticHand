import lexer as lx
import syntax as sx
import semantic as sm
import code_generator as cg
import pprint


# Variables globales
tree = ()  # Arbol de parseo
lines_with_errors = []  # Lista de lineas con los errores
flag_errors_found = False


# Inicia la compilación del código
def compiling(app):
    global tree
    global lines_with_errors
    global flag_errors_found
    flag_errors_found = False
    lines_with_errors = []

    app.log("Compilando...\n")
    lx.clear()
    sx.clear()
    sm.clear()
    cg.clear()

    # Analisis lexico
    lx.lexer.input(app.get_text())
    while True:
        tok = lx.lexer.token()
        if not tok:
            break
        elif app.lockDebug.get() == 1:
            app.log(str(tok) + "\n")
    if lx.get_error() != "":  # Detiene la compilacion: ERROR LEXICO
        app.log("Errores léxicos encontrados:\n", type_msg="warning")
        flag_errors_found = True
        lines_with_errors += lx.get_lines_error()
        highlight_errors(app)
        app.log(lx.get_error() + "\n", type_msg="error")
        return
    lx.clear()
    app.log("No se encontraron errores léxicos.\n")

    # Analisis sintactico
    tree = sx.run_parser(app.get_text())
    if sx.get_error() != "":  # Detiene la compilacion: ERROR SINTACTICO
        app.log("Errores sintácticos encontrados:\n", type_msg="warning")
        flag_errors_found = True
        lines_with_errors += sx.get_lines_error()
        app.log(sx.get_error(), type_msg="error")
        highlight_errors(app)
        return
    if app.lockDebug.get() == 1:
        tree_print = pprint.pformat(tree)
        app.log("\nArbol de parseo:\n", type_msg="info")
        app.log(tree_print + "\n\n")
    app.log("No se encontraron errores sintácticos.\n")

    # Analisis semantico
    global_vars = sm.check_semantics(tree)
    if sm.get_error() != "":  # Detiene la compilacion: ERROR SEMANTICO
        app.log("Errores semánticos encontrados:\n", type_msg="warning")
        flag_errors_found = True
        app.log(sm.get_error(), type_msg="error")
        lines_with_errors += sm.get_lines_error()
        highlight_errors(app)
        return
    if app.lockDebug.get() == 1:
        dict_vars = pprint.pformat(sm.variables)
        app.log("\nTabla de símbolos:\n", type_msg="info")
        app.log(dict_vars + "\n\n")
    app.log("No se encontraron errores semánticos.\n")

    # Generador de codigo
    cg.set_global_vars(global_vars)
    cg.translate(tree)
    cg.write_code()

    app.log("\nCompilación finalizada sin errores.\n\n", type_msg="success")


# Inicia la compilación y ejecución del código
def compiling_running(app):
    global flag_errors_found
    compiling(app)

    if flag_errors_found:
        return False

    app.log("Ejecutando...\n")
    return True


# Resalta las lineas con error en el IDE
def highlight_errors(app):
    global lines_with_errors
    for i in lines_with_errors:
        app.highlight(i)
