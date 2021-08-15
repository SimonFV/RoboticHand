import tkinter as tk

root = tk.Tk()


class App:
    def __init__(self, master):

        # Configuración de la ventana

        master.title("RoboticHand IDE")
        master.geometry("800x600")
        master.configure(bg="gray20")
        master.iconbitmap("img/robohand_ico.ico")

        # Frames para dividir la interfaz en secciones

        self.optionsFrame = tk.Frame(master, bg="gray20")
        self.optionsFrame.pack(ipady=5, ipadx=5, pady=5, padx=5, fill=tk.X, side=tk.TOP)

        self.codeFrame = tk.Frame(master, bg="gray15")
        self.codeFrame.pack(ipady=5, ipadx=5, pady=5, padx=5, fill=tk.BOTH, expand=1)

        self.logFrame = tk.Frame(master, bg="gray20")
        self.logFrame.pack(ipady=30, ipadx=5, pady=5, padx=5, fill=tk.X, side=tk.BOTTOM)

        # Botones

        self.newImg = tk.PhotoImage(file="img/new_img.png")
        self.newButton = tk.Button(
            self.optionsFrame,
            text="Nuevo",
            command=self.new,
            image=self.newImg,
            borderwidth=0,
            bg="gray20",
            activebackground="gray25",
        ).pack(ipadx=3, ipady=3, padx=5, side=tk.LEFT)

        self.loadImg = tk.PhotoImage(file="img/load_img.png")
        self.loadButton = tk.Button(
            self.optionsFrame,
            text="Cargar",
            command=self.load,
            image=self.loadImg,
            borderwidth=0,
            bg="gray20",
            activebackground="gray25",
        ).pack(ipadx=3, ipady=3, padx=5, side=tk.LEFT)

        self.saveImg = tk.PhotoImage(file="img/save_img.png")
        self.saveButton = tk.Button(
            self.optionsFrame,
            text="Guardar",
            command=self.save,
            image=self.saveImg,
            borderwidth=0,
            bg="gray20",
            activebackground="gray25",
        ).pack(ipadx=3, ipady=3, padx=5, side=tk.LEFT)

        self.compImg = tk.PhotoImage(file="img/comp_img.png")
        self.compButton = tk.Button(
            self.optionsFrame,
            text="Compilar",
            command=self.compile,
            image=self.compImg,
            borderwidth=0,
            bg="gray20",
            activebackground="gray25",
        ).pack(ipadx=3, ipady=3, padx=5, side=tk.LEFT)

        self.runImg = tk.PhotoImage(file="img/run_img.png")
        self.runButton = tk.Button(
            self.optionsFrame,
            text="Comp/Ejec",
            command=self.compile_run,
            image=self.runImg,
            borderwidth=0,
            bg="gray20",
            activebackground="gray25",
        ).pack(ipadx=3, ipady=3, padx=5, side=tk.LEFT)

        # Labels

        self.outLabel = tk.Label(
            self.logFrame,
            text="Output:",
            bg="gray20",
            fg="gray70",
            anchor="w",
            font=("Arial Black", 12),
        ).pack(side=tk.TOP, fill=tk.X)

        self.logLabel = tk.Label(self.logFrame, bg="gray17").pack(
            fill=tk.BOTH, expand=1, side=tk.BOTTOM
        )

        self.fileLabel = tk.Label(
            self.optionsFrame,
            text="Archivo.txt",
            bg="gray20",
            fg="gray70",
            anchor="w",
            font=("Arial Black", 12),
        ).pack(padx=20, side=tk.LEFT, fill=tk.X)

    # ------------------------------------------------------------
    # Métodos
    # ------------------------------------------------------------

    # Crea un nuevo archivo
    def new(self):
        print("Nuevo archivo creado!!")

    # Carga un archivo con código
    def load(self):
        print("Archivo cargado!!")

    # Guarda el código en un archivo
    def save(self):
        print("Archivo guardado!!")

    # Compila el código
    def compile(self):
        print("Compilando!!")

    # Compila y ejecuta el código
    def compile_run(self):
        print("Compilando y ejecutando!!")


# Inicializa la aplicación
app = App(root)
root.mainloop()
