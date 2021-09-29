# ---------------------------------------------
# ANALISIS SEMANTICO
# ---------------------------------------------


variables = {}  # Tabla de simbolos { nombre/id : valor / [return,args,cuerpo,linea] }
semantic_error = ""
line_error = 1
flag_main_found = False
flag_return = False
flag_insde_while = False
value_return = []
infinite_loops = 0
lines_of_error = []
flag_break_found = False


def clear():
    global variables
    global semantic_error
    global line_error
    global flag_main_found
    global flag_return
    global flag_insde_while
    global value_return
    global lines_of_error
    global infinite_loops
    global flag_break_found
    infinite_loops = 0
    variables = {}
    semantic_error = ""
    line_error = 1
    flag_main_found = False
    flag_return = False
    flag_insde_while = False
    value_return = []
    lines_of_error = []
    flag_break_found = False


def get_error():
    global semantic_error
    return semantic_error


def get_lines_error():
    global lines_of_error
    return lines_of_error


def check_semantics(p):
    global variables
    global semantic_error
    test(p)
    if not flag_main_found:
        semantic_error += "No se encontró el procedimiento main().\n"
    else:
        test(("p_call", "main", [], variables["main.0"][3]))
    return global_variables()


# Prueba el arbol en busca de errores semanticos
def test(p):
    global line_error
    global variables
    global semantic_error
    global flag_return
    global value_return
    global lines_of_error
    global flag_main_found
    global flag_insde_while
    global infinite_loops
    global flag_break_found

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
                        + str(p[3])
                        + ": El procedimiento main no debe contener argumentos."
                        + "\n"
                    )
                    lines_of_error += [p[3]]
                    return
                if p[0] != "None":
                    semantic_error += (
                        "Línea "
                        + str(p[3])
                        + ": El procedimiento main no puede retornar valores."
                        + "\n"
                    )
                    lines_of_error += [p[3]]
                    return
                flag_main_found = True

            if func_id in variables:
                semantic_error += (
                    "Línea "
                    + str(p[3])
                    + ": La función "
                    + str(p[1])
                    + " ya está definida."
                    + "\n"
                )
                lines_of_error += [p[3]]
                return
            variables[func_id] = [p[0], args, p[2], p[3]]

        # Llamada de funciones
        elif p[0] == "f_call" or p[0] == "p_call":
            func_id = p[1] + "." + str(len(p[2]))
            if not is_var_defined(func_id):
                return
            value_return += [[]]
            new_args = p[2]
            args = variables[func_id][1]
            for i in range(len(new_args)):
                var = test(new_args[i])
                if var == None:
                    return
                test(("=", args[i], var))
            test(variables[func_id][2])
            l_value_return = value_return.pop()

            if (
                variables[func_id][0] == "integer"
                and not test_value_return(l_value_return, 3)
            ) or (
                variables[func_id][0] == "boolean"
                and not test_value_return(l_value_return, True)
            ):
                semantic_error += (
                    "Línea "
                    + str(variables[func_id][3])
                    + ": Los valores de retorno de la función [ "
                    + p[1]
                    + " ] deben ser "
                    + variables[func_id][0]
                    + ".\n"
                )
                lines_of_error += [variables[func_id][3]]
                return None
            if variables[func_id][0] == "None" and len(l_value_return) != 0:
                semantic_error += (
                    "Línea "
                    + str(variables[func_id][3])
                    + ": El procedimiento [ "
                    + p[1]
                    + " ] no puede retornar un valor.\n"
                )
                lines_of_error += [variables[func_id][3]]
                return None
            if len(l_value_return) != 0 and p[0] == "p_call":
                semantic_error += (
                    "Línea "
                    + str(p[3])
                    + ": El valor de retorno de la función [ "
                    + p[1]
                    + " ] debe ser capturado.\n"
                )
                lines_of_error += [p[3]]
                return None
            if len(l_value_return) == 0 and p[0] == "f_call":
                semantic_error += (
                    "Línea "
                    + str(p[3])
                    + ": El procedimiento [ "
                    + p[1]
                    + " ] no retorna un valor.\n"
                )
                lines_of_error += [p[3]]
                return None
            if len(l_value_return) == 0:
                return None
            return l_value_return[0]

        # Retorno de funciones
        elif p[0] == "return":
            if p[1] == None:
                value_return[len(value_return) - 1] += []
            else:
                value_return[len(value_return) - 1] += [test(p[1])]
            return

        # Asignacion de variables
        elif p[0] == "=":
            var = test(p[2])
            if var == None:
                semantic_error += (
                    "Línea "
                    + str(p[3])
                    + ": Valor de asignación para "
                    + p[1]
                    + " no especificado.\n"
                )
                lines_of_error += [p[3]]
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
                lines_of_error += [p[3]]
            else:
                variables[p[1]] = var

        # Iteraciones
        elif p[0] == "for=" or p[0] == "for":
            if type(test(p[1][1])) != int or type(test(p[1][2])) != int:
                semantic_error += (
                    "Línea "
                    + str(p[3])
                    + ": Los dos valores del rango deben ser enteros."
                    + "\n"
                )
                lines_of_error += [p[3]]
                return
            test(("=", p[1][0], p[1][1], p[3]))
            test(p[2])
        elif p[0] == "while" or p[0] == "loop":
            if p[0] == "while":
                expr = test(p[1])
                if type(expr) != bool:
                    semantic_error += (
                        "Línea "
                        + str(p[3])
                        + ": La condición del iterador debe ser boolean."
                        + "\n"
                    )
                    lines_of_error += [p[3]]
                    return
                if p[1] == True:
                    infinite_loops += 1
                elif type(p[1]) == tuple:
                    if type(p[1][1]) != tuple and type(p[1][2]) != tuple:
                        if type(p[1][1]) != str and type(p[1][2]) != str:
                            infinite_loops += 1
            else:
                infinite_loops += 1
            flag_break_found = False
            local_infinite_loop = infinite_loops
            local_inside_while = flag_insde_while
            flag_insde_while = True
            test(p[2])
            if not local_inside_while:
                flag_insde_while = False
            flag_break_found = False
            if local_infinite_loop != 0 and local_infinite_loop == infinite_loops:
                semantic_error += (
                    "Línea " + str(p[3]) + ": Loop infinito sin break." + "\n"
                )
                lines_of_error += [p[3]]
                if local_inside_while:
                    infinite_loops += 1
        elif p[0] == "break":
            if flag_break_found:
                return
            if not flag_insde_while:
                semantic_error += (
                    "Línea "
                    + str(p[3])
                    + ": El break debe ir dentro de un while o de un loop."
                    + "\n"
                )
                lines_of_error += [p[3]]
                return
            infinite_loops -= 1
            flag_break_found = True

        # If - else
        elif p[0] == "if" or p[0] == "if-else":
            expr = test(p[1])
            if type(expr) != bool:
                semantic_error += (
                    "Línea "
                    + str(p[3])
                    + ": La condición del if debe ser boolean."
                    + "\n"
                )
                lines_of_error += [p[3]]
                return
            test(p[2])

        # Mover los dedos
        elif p[0] == "Move":
            for i in p[1]:
                if (
                    (type(i) != tuple)
                    or (i[0] != "text")
                    or (
                        (i[1] != '"P"')
                        and (i[1] != '"I"')
                        and (i[1] != '"M"')
                        and (i[1] != '"A"')
                        and (i[1] != '"Q"')
                        and (i[1] != '"T"')
                    )
                ):
                    semantic_error += (
                        "Línea "
                        + str(p[3])
                        + ': Primer argumento incorrecto. Valores aceptados para dedos: "P", "I", "M", "A", "Q", "T"'
                        + '\nTambién se pueden ingresar como lista: ["P", "I"]\n'
                    )
                    lines_of_error += [p[3]]
                    return
            if type(test(p[2])) != bool:
                semantic_error += (
                    "Línea "
                    + str(p[3])
                    + ": Segundo argumento incorrecto. Solo se aceptan tipo boolean.\n"
                )
                lines_of_error += [p[3]]
                return

        # Delay
        elif p[0] == "Delay":
            expr = test(p[1])
            if (type(expr) != int) or (expr < 0):
                semantic_error += (
                    "Línea "
                    + str(p[3])
                    + ": Primer argumento incorrecto. Se debe utilizar un entero positivo.\n"
                )
                lines_of_error += [p[3]]
                return
            if (
                (type(p[2]) != tuple)
                or (p[2][0] != "text")
                or (
                    (p[2][1] != '"Seg"')
                    and (p[2][1] != '"Mil"')
                    and (p[2][1] != '"Min"')
                )
            ):
                semantic_error += (
                    "Línea "
                    + str(p[3])
                    + ': Segundo argumento incorrecto. Se aceptan los parámetros "Seg", "Mil", "Min"\n'
                )
                lines_of_error += [p[3]]
                return

        # Operaciones matematicas
        elif p[0] == "+":
            if type(test(p[1])) == int and type(test(p[2])) == int:
                return test(p[1]) + test(p[2])
            semantic_error += (
                "Línea " + str(p[3]) + ": Ambos operandos deben ser enteros." + "\n"
            )
            lines_of_error += [p[3]]
            return None
        elif p[0] == "-":
            if type(test(p[1])) == int and type(test(p[2])) == int:
                return test(p[1]) - test(p[2])
            semantic_error += (
                "Línea " + str(p[3]) + ": Ambos operandos deben ser enteros." + "\n"
            )
            lines_of_error += [p[3]]
            return None
        elif p[0] == "*":
            if type(test(p[1])) == int and type(test(p[2])) == int:
                return test(p[1]) * test(p[2])
            semantic_error += (
                "Línea " + str(p[3]) + ": Ambos operandos deben ser enteros." + "\n"
            )
            lines_of_error += [p[3]]
            return None
        elif p[0] == "/":
            if type(test(p[1])) == int and type(test(p[2])) == int:
                return int(test(p[1]) / test(p[2]))
            semantic_error += (
                "Línea " + str(p[3]) + ": Ambos operandos deben ser enteros." + "\n"
            )
            lines_of_error += [p[3]]
            return None
        elif p[0] == "**":
            if type(test(p[1])) == int and type(test(p[2])) == int:
                return int(test(p[1]) ** test(p[2]))
            semantic_error += (
                "Línea " + str(p[3]) + ": Ambos operandos deben ser enteros." + "\n"
            )
            lines_of_error += [p[3]]
            return None

        # Operaciones logicas
        elif p[0] == "|":
            if type(test(p[1])) == bool and type(test(p[2])) == bool:
                return test(p[1]) or test(p[2])
            semantic_error += (
                "Línea " + str(p[3]) + ": Ambos operandos deben ser booleanos." + "\n"
            )
            lines_of_error += [p[3]]
            return None
        elif p[0] == "&":
            if type(test(p[1])) == bool and type(test(p[2])) == bool:
                return test(p[1]) and test(p[2])
            semantic_error += (
                "Línea " + str(p[3]) + ": Ambos operandos deben ser booleanos." + "\n"
            )
            lines_of_error += [p[3]]
            return None

        # Comparaciones
        elif p[0] == "<>":
            if type(test(p[1])) == type(test(p[2])):
                return test(p[1]) != test(p[2])
            semantic_error += (
                "Línea "
                + str(p[3])
                + ": Ambos operandos deben ser del mismo tipo en la comparación."
                + "\n"
            )
            lines_of_error += [p[3]]
            return None
        elif p[0] == "==":
            if type(test(p[1])) == type(test(p[2])):
                return test(p[1]) == test(p[2])
            semantic_error += (
                "Línea "
                + str(p[3])
                + ": Ambos operandos deben ser del mismo tipo en la comparación."
                + "\n"
            )
            lines_of_error += [p[3]]
            return None
        elif p[0] == "<":
            if type(test(p[1])) == type(test(p[2])):
                return test(p[1]) < test(p[2])
            semantic_error += (
                "Línea "
                + str(p[3])
                + ": Ambos operandos deben ser del mismo tipo en la comparación."
                + "\n"
            )
            lines_of_error += [p[3]]
            return None
        elif p[0] == ">":
            if type(test(p[1])) == type(test(p[2])):
                return test(p[1]) > test(p[2])
            semantic_error += (
                "Línea "
                + str(p[3])
                + ": Ambos operandos deben ser del mismo tipo en la comparación."
                + "\n"
            )
            lines_of_error += [p[3]]
            return None
        elif p[0] == "<=":
            if type(test(p[1])) == type(test(p[2])):
                return test(p[1]) <= test(p[2])
            semantic_error += (
                "Línea "
                + str(p[3])
                + ": Ambos operandos deben ser del mismo tipo en la comparación."
                + "\n"
            )
            lines_of_error += [p[3]]
            return None
        elif p[0] == ">=":
            if type(test(p[1])) == type(test(p[2])):
                return test(p[1]) >= test(p[2])
            semantic_error += (
                "Línea "
                + str(p[3])
                + ": Ambos operandos deben ser del mismo tipo en la comparación."
                + "\n"
            )
            lines_of_error += [p[3]]
            return None

        # Print
        elif p[0] == "print":
            for i in p[1]:
                test(i)
        elif p[0] == "text":
            return p[1]

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


def test_value_return(return_list, t):
    if len(return_list) == 0:
        return False

    for i in return_list:
        if type(i) != type(t):
            return False
    return True


def global_variables():
    global variables
    global_vars = ""
    for i in variables:
        if type(variables[i]) != list:
            global_vars += "\tglobal " + str(i) + "_var\n"
    return global_vars
