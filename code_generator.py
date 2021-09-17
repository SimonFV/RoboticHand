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
            temp = p[1][0].replace("#", "_num_s_").replace("?", "_qust_s_")
            code += "def " + temp + "("
            if len(args) != 0:
                for i in args:
                    code += i + ","
                code = code[:-1]
            code += "):\n"
            if temp == "main":
                code += "\trobohand_app.update_idletasks()\n\trobohand_app.update()\n\n"
            translate(p[2])
            scope -= 1
            code += "\n\n"

        # Llamada de funciones
        elif p[0] == "call":
            temp = p[1].replace("#", "_num_s_").replace("?", "_qust_s_")
            code += ("\t" * scope) + temp + "("
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
            temp = p[1].replace("#", "_num_s_").replace("?", "_qust_s_")
            code += ("\t" * scope) + temp + " = "
            translate(p[2])
            code += "\n"

        # Iteradores
        elif p[0] == "for=" or p[0] == "for":
            code += ("\t" * scope) + "for " + p[1][0] + " in range("
            translate(p[1][1])
            code += ", "
            if p[0] == "for=":
                translate(p[1][2] + 1)
            else:
                translate(p[1][2])
            code += "):\n"
            scope += 1
            translate(p[2])
            scope -= 1
            code += "\n"
        elif p[0] == "while" or p[0] == "loop":
            if p[0] == "while":
                code += ("\t" * scope) + "while ("
                translate(p[1])
                code += "):\n"
            else:
                code += ("\t" * scope) + "while True:\n"
            scope += 1
            translate(p[2])
            scope -= 1
            code += "\n"

        # Break
        elif p[0] == "break":
            code += ("\t" * scope) + "break\n"

        # If - else - elif
        elif p[0] == "if" or p[0] == "if-else":
            code += ("\t" * scope) + "if "
            translate(p[1])
            code += ":\n"
            scope += 1
            if p[0] == "if-else":
                translate(p[2][0])
                scope -= 1
                code += "\n"
                code += ("\t" * scope) + "else:\n"
                scope += 1
                translate(p[2][1])
                scope -= 1
                code += "\n"
            else:
                translate(p[2])
                scope -= 1
                code += "\n"

        # Move
        elif p[0] == "Move":
            code += ("\t" * scope) + "robohand_Move(["
            for i in p[1]:
                translate(i)
                code += ","
            code = code[:-1]
            code += "], "
            translate(p[2])
            code += ")\n"

        # Delay
        elif p[0] == "Delay":
            code += ("\t" * scope) + "robohand_Delay("
            translate(p[1])
            code += ", "
            translate(p[2])
            code += ")\n"

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

        # Comparaciones
        elif (
            p[0] == "=="
            or p[0] == "<>"
            or p[0] == "<="
            or p[0] == ">="
            or p[0] == "<"
            or p[0] == ">"
        ):
            code += "("
            translate(p[1])
            code += " " + p[0] + " "
            translate(p[2])
            code += ")"

        # Print
        elif p[0] == "print":
            code += ("\t" * scope) + "robohand_println("
            for i in p[1]:
                code += "str("
                translate(i)
                code += ")+"
            code = code[:-1]
            code += ")\n"
        elif p[0] == "text":
            code += p[1]

        # Recorre el resto del arbol
        else:
            for i in range(len(p)):
                translate(p[i])

    # Si no es una tupla y es una variable o una constante
    else:
        temp = str(p)
        temp = temp.replace("#", "_num_s_")
        temp = temp.replace("?", "_qust_s_")
        code += temp


# Crea los archivos de python necesarios para ejecutar el codigo
def write_code(app):
    global code

    # Agrega la funcion para imprimir en el IDE
    pre_code = """from tkinter import Tk
from tkinter import Text
from tkinter import Scrollbar

robohand_app = Tk()
robohand_app.title("RoboticHand App")
robohand_app.geometry("800x600")
robohand_app.configure(bg="gray18")

robohand_outScroll = Scrollbar(robohand_app)
robohand_logText = Text(
    robohand_app,
    font=("Consolas", 13),
    height=8,
    background="gray18",
    foreground="gray90",
    selectbackground="magenta4",
    selectforeground="gray90",
    insertbackground="magenta2",
    yscrollcommand=robohand_outScroll.set,
    borderwidth=0,
)
robohand_logText.pack(
    ipady=5, ipadx=5, pady=5, padx=5, fill="both", side="left", expand=True
)
robohand_outScroll.config(command=robohand_logText.yview)
robohand_outScroll.pack(fill="y", side="right")
robohand_logText.config(state="disabled")


def robohand_println(msg):
    robohand_logText.config(state="normal")
    robohand_logText.insert("end", msg + \"\\n\")
    robohand_logText.see("end")
    robohand_logText.config(state="disabled")
    robohand_app.update_idletasks()
    robohand_app.update()

def robohand_Delay(robohand_num, robohand_scale):
    robohand_println(\"Delay: \" + str(robohand_num) + \" \" + robohand_scale)
    robohand_app.update_idletasks()
    robohand_app.update()

def robohand_Move(robohand_fingers, robohand_side):
    robohand_println(\"Move: \" + str(robohand_fingers) + \" \" + str(robohand_side))
    robohand_app.update_idletasks()
    robohand_app.update()


"""
    code = pre_code + code + "\nmain()\nrobohand_app.mainloop()\n"

    exeFile = open("program.py", "w")
    exeFile.write(code)
    exeFile.close()
