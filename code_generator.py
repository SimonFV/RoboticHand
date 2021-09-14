import sys

scope = 0
code = ""

# Limpia las variables globales
def clear():
    global code
    global scope
    code = ""
    scope = 0


# Inicia la conversion de codigo desde el arbol a un archivo con codigo python
def translate(p):
    global scope
    global code

    if type(p) == tuple:

        # Definicion de funciones
        if p[0] == "integer" or p[0] == "boolean" or p[0] == "None":
            scope += 1
            args = p[1][1:]
            code += "def " + p[1][0] + "("
            if len(args) != 0:
                for i in args:
                    code += i + ","
                code = code[:-1]
            code += "):\n"
            translate(p[2])
            scope -= 1
            code += "\n\n"

        # Llamada de funciones
        elif p[0] == "call":
            code += ("\t" * scope) + p[1] + "("
            if len(p[2]) != 0:
                for i in p[2]:
                    translate(i)
                    code += ","
                code = code[:-1]
            code += ")\n"
            return

        # Return de funciones
        elif p[0] == "return":
            code += ("\t" * scope) + "return "
            translate(p[1])
            code += "\n"

        # Asignacion de variables
        elif p[0] == "=":
            code += ("\t" * scope) + p[1] + " = "
            translate(p[2])
            code += "\n"

        # Operaciones matematicas
        elif p[0] == "+" or p[0] == "-" or p[0] == "*":
            code += "("
            translate(p[1])
            code += p[0]
            translate(p[2])
            code += ")"
        elif p[0] == "/" or p[0] == "**":
            code += "int("
            translate(p[1])
            code += p[0]
            translate(p[2])
            code += ")"

        # Operaciones logicas
        elif p[0] == "|":
            code += "("
            translate(p[1])
            code += " or "
            translate(p[2])
            code += ")"
        elif p[0] == "&":
            code += "("
            translate(p[1])
            code += " and "
            translate(p[2])
            code += ")"

        # Recorre el resto del arbol
        else:
            for i in range(len(p)):
                translate(p[i])

    # Si no es una tupla y es una variable o una constante
    else:
        code += str(p)


# Crea los archivos de python necesarios para ejecutar el codigo
def write_code(app):
    global code

    exeFile = open("script.py", "w")
    exeFile.write(code)
    exeFile.close()

    exe_script = "import script\n\nscript.main()\n"

    exeFile = open("exe.py", "w")
    exeFile.write(exe_script)
    exeFile.close()

