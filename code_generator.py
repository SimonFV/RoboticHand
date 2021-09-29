import sys

scope = 1
code = ""
global_vars = ""

# Limpia las variables globales
def clear():
    global code
    global scope
    code = ""
    scope = 1


def set_global_vars(global_vars_p):
    global global_vars
    global_vars = global_vars_p


# Inicia la conversion de codigo desde el arbol a un archivo con codigo python
def translate(p):
    global global_vars
    global scope
    global code

    if type(p) == tuple:

        # Definicion de funciones
        if p[0] == "integer" or p[0] == "boolean" or p[0] == "None":
            scope += 1
            args = p[1][1:]
            name = p[1][0].replace("#", "_num_s_").replace("?", "_qust_s_")
            name += "_" + str(len(args))
            code += "def " + name + "("
            if len(args) != 0:
                for i in args:
                    code += i + "_arg" + ","
                code = code[:-1]
            code += "):\n"
            if name == "main_0":
                code += '\trobohand_println("Listo!", "debug")\n\trobohand_app.update_idletasks()\n\trobohand_app.update()\n'
            code += global_vars
            all_vars = global_vars.split("\n")
            for arg in args:
                for var in all_vars:
                    if var == ("\tglobal " + arg + "_var"):
                        code += "\t" + arg + "_var = " + arg + "_arg\n"
            code += "\ttry:\n"
            translate(p[2])
            scope -= 1
            code += "\texcept Exception as ex:\n\t\trobohand_print_exception(ex)\n\n"

        # Llamada de funciones
        elif p[0] == "f_call" or p[0] == "p_call":
            name = p[1].replace("#", "_num_s_").replace("?", "_qust_s_")
            name += "_" + str(len(p[2]))
            if p[0] == "p_call":
                code += "\t" * scope
            code += name + "("
            if len(p[2]) != 0:
                for i in p[2]:
                    translate(i)
                    code += ","
                code = code[:-1]
            code += ")"
            if p[0] == "p_call":
                code += "\n"
            return

        # Return de funciones
        elif p[0] == "return":
            code += ("\t" * scope) + "return "
            translate(p[1])
            code += "\n"

        # Asignacion de variables
        elif p[0] == "=":
            temp = p[1].replace("#", "_num_s_").replace("?", "_qust_s_")
            code += ("\t" * scope) + temp + "_var" + " = "
            translate(p[2])
            code += "\n"

        # Iteradores
        elif p[0] == "for=" or p[0] == "for":
            code += ("\t" * scope) + "for " + p[1][0] + "_var in range("
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
        if type(p) != str:
            code += temp
        else:
            code += temp + "_var"


# Crea los archivos de python necesarios para ejecutar el codigo
def write_code():
    global code

    # Agrega la funcion para imprimir en el IDE
    pre_code = """from tkinter import Tk
from tkinter import Text
from tkinter import Scrollbar
from tkinter import Checkbutton
from tkinter import IntVar
from time import sleep
import serial


robohand_ser_arduino = None

robohand_app = Tk()
robohand_app.title("RoboticHand App")
robohand_app.geometry("800x600")
robohand_app.configure(bg="gray18")

robohand_debug = IntVar(value=1)
robohand_lockDebug = Checkbutton(
    robohand_app,
    text="Debug",
    borderwidth=0,
    bg="gray22",
    fg="gray80",
    font=("Arial", 10),
    activebackground="gray40",
    variable=robohand_debug,
    onvalue=1,
    offvalue=0,
)
robohand_lockDebug.pack(fill="x", side="top")

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
robohand_logText.tag_configure("debug", foreground="deep sky blue")
robohand_logText.tag_configure("error", foreground="salmon")
robohand_logText.tag_configure("normal", foreground="gray90")


def robohand_init():
    global robohand_ser_arduino
    usbport = "COM5"

    robohand_println("Conectando con la mano...", "debug")
    try:
        robohand_ser_arduino = serial.Serial(usbport, 9600, timeout=2)
    except:
        robohand_println("Error al conectar con el puerto serial.", "error")
        robohand_println(
            "Revise la conexion o verifique que no haya otro programa ya conectado."
        )
        robohand_println("Ejecucion detenida.", "debug")
        return
    robohand_app.after(3000, main_0)


def robohand_print_exception(ex):
    if type(ex).__name__ != "NameError":
        robohand_println("Error desconocido durante la ejecucion.", "error")
        return
    tb = ex.__traceback__
    if tb is not None:
        name_var = str(ex).split()[1].strip("'")
        name_var = name_var[:-4]
        name_func = tb.tb_frame.f_code.co_name.split("_")
        func = ""
        for i in range(len(name_func) - 1):
            func += name_func[i]
        robohand_println(
            "Variable "
            + name_var
            + " llamada antes de definirse, en la funcion "
            + func,
            "error"
        )


def robohand_println(robohand_msg, robohan_debug_type="normal"):
    robohand_logText.config(state="normal")
    robohand_logText.insert("end", robohand_msg + "\\n", robohan_debug_type)
    robohand_logText.see("end")
    robohand_logText.config(state="disabled")
    robohand_app.update_idletasks()
    robohand_app.update()


def robohand_Delay(robohand_num, robohand_scale):
    global robohand_debug
    if robohand_debug.get() == 1:
        robohand_println("Delay: " + str(robohand_num) + " " + robohand_scale, "debug")
        robohand_app.update_idletasks()
        robohand_app.update()
    scale = 1
    if robohand_scale == "Min":
        scale = 60
    elif robohand_scale == "Mil":
        scale = 0.001
    sleep(robohand_num * scale)


def robohand_Move(robohand_fingers, robohand_side):
    global robohand_debug
    global robohand_ser_arduino
    if robohand_debug.get() == 1:
        robohand_println(
            "Move: " + str(robohand_fingers) + " " + str(robohand_side), "debug"
        )
        robohand_app.update_idletasks()
        robohand_app.update()

    robohand_msg = ""
    robohand_angle = "180"
    if robohand_side:
        robohand_angle = "090"
    for robohand_finger in robohand_fingers:
        if robohand_finger == "P":
            robohand_msg += "1," + robohand_angle + "b"
        elif robohand_finger == "I":
            robohand_msg += "2," + robohand_angle + "b"
        elif robohand_finger == "M":
            robohand_msg += "3," + robohand_angle + "b"
        elif robohand_finger == "A":
            robohand_msg += "4," + robohand_angle + "b"
        elif robohand_finger == "Q":
            robohand_msg += "5," + robohand_angle + "b"
        elif robohand_finger == "T":
            robohand_msg += "6," + robohand_angle + "b"
        else:
            return

    try:
        robohand_ser_arduino.write(robohand_msg.encode())
    except:
        robohand_println("Problema al enviar el mensaje a la mano", "error");


"""
    code = pre_code + code + "\nrobohand_init()\nrobohand_app.mainloop()\n"
    code = code.encode("ascii", "ignore")
    code = code.decode("utf-8", "ignore")

    exeFile = open("program.py", "w")
    exeFile.write(code)
    exeFile.close()
