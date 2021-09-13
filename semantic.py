# ---------------------------------------------
# ANALISIS SEMANTICO
# ---------------------------------------------


variables = {}  # Tabla de simbolos { nombre/id : valor / [return, args, cuerpo] }
semantic_error = ""
line_error = 1
flag_main_found = False
flag_return = False
value_return = None
lines_of_error = []


def clear():
    global semantic_error
    global variables
    global line_error
    global lines_of_error
    global flag_main_found
    semantic_error = ""
    variables = {}
    line_error = 1
    lines_of_error = []
    flag_main_found = False


def get_error():
    global semantic_error
    return semantic_error


def get_lines_error():
    global lines_of_error
    return lines_of_error


def check_semantics(p):
    global variables
    global semantic_error
    print(p)
    test(p)
    if not flag_main_found:
        semantic_error += "No se encontró la función main().\n"
    print(variables)


# Prueba el arbol en busca de errores semanticos
def test(p):
    global line_error
    global variables
    global semantic_error
    global flag_return
    global value_return
    global lines_of_error
    global flag_main_found

    if flag_return:
        return

    if type(p) == tuple:
        # Registro de la linea actual
        if len(p) == 4:
            line_error = p[3]

        # Definicion de funciones
        if p[0] == "integer" or p[0] == "boolean" or p[0] == "None":
            func_id = p[1][0] + "." + str(len(p[1]) - 1)
            args = p[1][1:]
            if p[1][0] == "main":
                if len(args) != 0:
                    semantic_error += (
                        "Línea "
                        + str(line_error)
                        + ": La función main no debe contener argumentos."
                        + "\n"
                    )
                    lines_of_error += [line_error]
                    return
                flag_main_found = True
                test(p[2])
                return

            elif func_id in variables:
                semantic_error += (
                    "Línea "
                    + str(line_error)
                    + ": La función "
                    + str(p[1])
                    + " ya está definida."
                    + "\n"
                )
                lines_of_error += [line_error]
                return
            variables[func_id] = [p[0], args, p[2]]

        # Llamada de funciones
        elif p[0] == "call":
            value_return = None
            func_id = p[1] + "." + str(len(p[2]))
            if not is_var_defined(func_id):
                return
            new_args = p[2]
            args = variables[func_id][1]
            for i in range(len(new_args)):
                var = test(new_args[i])
                if var == None:
                    return
                test(("=", args[i], var))
                print(args[i], var)
            test(variables[func_id][2])
            flag_return = False
            for arg in args:
                variables.pop(arg)
            if (variables[func_id][0] == "integer" and type(value_return) != int) or (
                variables[func_id][0] == "boolean" and type(value_return) != bool
            ):
                semantic_error += (
                    "Línea "
                    + str(p[3])
                    + ": Valor de retorno debe ser "
                    + variables[func_id][0]
                    + ".\n"
                )
                lines_of_error += [p[3]]
                return None
            if variables[func_id][0] == "None" and value_return != None:
                semantic_error += (
                    "Línea "
                    + str(line_error)
                    + ": La función no puede retornar un valor.\n"
                )
                lines_of_error += [line_error]
                return None
            return value_return

        # Return de funciones
        elif p[0] == "return":
            if p[1] == None:
                value_return = None
            else:
                value_return = test(p[1])
            flag_return = True
            return

        # Asignacion de variables
        elif p[0] == "=":
            var = test(p[2])
            if var == None:
                semantic_error += (
                    "Línea " + str(p[3]) + ": Valor de retorno no especificado.\n"
                )
                lines_of_error += [p[3]]
                return
            if (p[1] in variables) and type(variables[p[1]]) != type(var):
                semantic_error += (
                    "Línea "
                    + str(line_error)
                    + ": La variable "
                    + str(p[1])
                    + " está definida con otro tipo."
                    + "\n"
                )
                lines_of_error += [line_error]
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
            lines_of_error += [line_error]
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
            lines_of_error += [line_error]
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
            lines_of_error += [line_error]
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
            lines_of_error += [line_error]
            return None
        elif p[0] == "**":
            if type(test(p[1])) == int and type(test(p[2])) == int:
                return int(test(p[1]) ** test(p[2]))
            semantic_error += (
                "Línea "
                + str(line_error)
                + ": Ambos operandos deben ser enteros."
                + "\n"
            )
            lines_of_error += [line_error]
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
            lines_of_error += [line_error]
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
            lines_of_error += [line_error]
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
    global lines_of_error
    global semantic_error
    try:
        var = variables[var]
    except LookupError:
        semantic_error += (
            "Línea "
            + str(line_error)
            + ": Identificador no definido: "
            + var.split(".")[0]
            + "\n"
        )
        lines_of_error += [line_error]
        return False
    return True
