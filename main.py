from os import spawnl
from posixpath import split
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font
import tkinter.ttk
import tkinter as tk
import ntpath
import compilation as comp

# Canvas para los numeros de las lineas
class customLineCanvas(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None
        self.fontSize = 12
        self.font = tkinter.font.Font(family="monospace", size=self.fontSize)

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        self.delete("all")
        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(
                1, y + 1, anchor="nw", font=self.font, text=linenum, fill="cyan3"
            )
            i = self.textwidget.index("%s+1line" % i)


# Clase principal
class App:
    def __init__(self, master):

        # Algunos atributos
        self.fileRute = ""
        self.fileName = ""
        self.isShown = True

        # Configuración de la ventana

        master.title("RoboticHand IDE")
        master.geometry("800x600")
        master.configure(bg="gray20")
        master.iconbitmap("img/robohand_ico.ico")
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Frames para dividir la interfaz en secciones

        self.optionsFrame = tk.Frame(master, bg="gray20")
        self.optionsFrame.pack(ipady=5, ipadx=5, pady=5, padx=5, fill=tk.X, side=tk.TOP)

        self.logFrame = tk.Frame(master, bg="gray20")
        self.logFrame.columnconfigure(0, weight=1)
        self.logFrame.rowconfigure(0, weight=1)
        self.logFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=5, pady=5)

        self.codeFrame = tk.Frame(master, bg="gray15")
        self.codeFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=5, pady=5, expand=True)

        # Botones

        self.newImg = tk.PhotoImage(file="img/new_img.png")
        self.newButton = tk.Button(
            self.optionsFrame,
            command=self.new,
            image=self.newImg,
            borderwidth=0,
            bg="gray20",
            activebackground="gray25",
        ).pack(ipadx=3, ipady=3, padx=5, side=tk.LEFT)

        self.loadImg = tk.PhotoImage(file="img/load_img.png")
        self.loadButton = tk.Button(
            self.optionsFrame,
            command=self.load,
            image=self.loadImg,
            borderwidth=0,
            bg="gray20",
            activebackground="gray25",
        ).pack(ipadx=3, ipady=3, padx=5, side=tk.LEFT)

        self.saveImg = tk.PhotoImage(file="img/save_img.png")
        self.saveButton = tk.Button(
            self.optionsFrame,
            command=self.save,
            image=self.saveImg,
            borderwidth=0,
            bg="gray20",
            activebackground="gray25",
        ).pack(ipadx=3, ipady=3, padx=5, side=tk.LEFT)

        self.compImg = tk.PhotoImage(file="img/comp_img.png")
        self.compButton = tk.Button(
            self.optionsFrame,
            command=self.compile_code,
            image=self.compImg,
            borderwidth=0,
            bg="gray20",
            activebackground="gray25",
        ).pack(ipadx=3, ipady=3, padx=5, side=tk.LEFT)

        self.runImg = tk.PhotoImage(file="img/run_img.png")
        self.runButton = tk.Button(
            self.optionsFrame,
            command=self.compile_run,
            image=self.runImg,
            borderwidth=0,
            bg="gray20",
            activebackground="gray25",
        ).pack(ipadx=3, ipady=3, padx=5, side=tk.LEFT)

        self.showButton = tk.Button(
            self.logFrame,
            text="Ocultar",
            command=self.hide_show_log,
            borderwidth=0,
            bg="gray22",
            fg="gray80",
            font=("Arial", 10),
            activebackground="gray40",
        )
        self.showButton.grid(row=0, column=1, padx=5)

        self.clearButton = tk.Button(
            self.logFrame,
            text="Limpiar",
            command=self.clear_log,
            borderwidth=0,
            bg="gray22",
            fg="gray80",
            font=("Arial", 10),
            activebackground="gray40",
        ).grid(row=0, column=2, padx=5)

        self.lockVar = tk.IntVar()
        self.lockButton = tk.Checkbutton(
            self.logFrame,
            text="Auto-scroll",
            borderwidth=0,
            bg="gray22",
            fg="gray80",
            font=("Arial", 10),
            activebackground="gray40",
            variable=self.lockVar,
            onvalue=1,
            offvalue=0,
        )
        self.lockButton.grid(row=0, column=3, padx=5)

        # Entry - Nombre del archivo
        self.fileEntry = tk.Entry(
            self.optionsFrame,
            bg="gray20",
            fg="gray70",
            font=("Arial Black", 12),
            selectbackground="cyan4",
            insertbackground="cyan2",
            borderwidth=0,
        )

        # Salida

        self.outputLabel = tk.Label(
            self.logFrame,
            text="Salida:",
            bg="gray20",
            fg="gray70",
            font=("Arial Black", 12),
        ).grid(row=0, column=0, sticky=tk.W)

        self.outScroll = tk.Scrollbar(self.logFrame)
        self.logText = tk.Text(
            self.logFrame,
            font=("Consolas", 13),
            height=8,
            background="gray18",
            selectbackground="magenta4",
            selectforeground="gray90",
            insertbackground="magenta2",
            yscrollcommand=self.outScroll.set,
            borderwidth=0,
        )
        self.logText.grid(row=1, column=0, columnspan=4, sticky=tk.NSEW)
        self.outScroll.config(command=self.logText.yview)
        self.outScroll.grid(row=1, column=4, sticky=tk.NS)
        self.logText.tag_configure("info", foreground="deep sky blue")
        self.logText.tag_configure("warning", foreground="yellow2")
        self.logText.tag_configure("error", foreground="orange red")
        self.logText.tag_configure("success", foreground="SpringGreen2")
        self.logText.tag_configure("normal", foreground="gray90")
        self.logText.config(state="disabled")

        # Edición de texto

        self.textScroll = tk.Scrollbar(self.codeFrame)
        self.textScrollx = tk.Scrollbar(self.codeFrame, orient="horizontal")
        self.codeText = tk.Text(
            self.codeFrame,
            font=("Consolas", 13),
            background="gray15",
            foreground="gray90",
            selectbackground="cyan4",
            selectforeground="gray90",
            insertbackground="cyan2",
            wrap="none",
            undo=True,
            yscrollcommand=self.on_text_scroll,
            xscrollcommand=self.textScrollx.set,
            borderwidth=0,
        )
        self.textScroll.config(command=self.scroll_both)
        self.textScrollx.config(command=self.codeText.xview)

        self.lineCanvas = customLineCanvas(
            self.codeFrame,
            width=40,
            background="gray17",
            borderwidth=0,
            highlightthickness=0,
        )
        self.lineCanvas.attach(self.codeText)

        self.textScroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.textScrollx.pack(side=tk.BOTTOM, fill=tk.X)
        self.codeText.pack(side=tk.RIGHT, padx=4, fill=tk.BOTH, expand=1)
        self.codeText.bind("<<Modified>>", self.line_update)
        self.codeText.tag_configure("error_line", background="red4")
        self.codeText.config(state="disabled")

    # ------------------------------------------------------------
    # Métodos
    # ------------------------------------------------------------

    # Crea un nuevo archivo
    def new(self):
        if not self.is_file_saved() and self.codeText.get("1.0", "end-1c") != "":
            response = tkinter.messagebox.askyesno(
                "Archivo no guardado ", "¿Guardar archivo?"
            )
            if response == 1:
                self.save()

        self.fileRute = ""
        self.fileName = "Nuevo_archivo"
        self.fileEntry.delete(0, tk.END)
        self.fileEntry.insert(0, self.fileName)
        self.activate_text()

    # Carga un archivo con código
    def load(self):
        if not self.is_file_saved() and self.codeText.get("1.0", "end-1c") != "":
            response = tkinter.messagebox.askyesno(
                "Archivo no guardado ", "¿Guardar archivo?"
            )
            if response == 1:
                self.save()

        loadedFile = tkinter.filedialog.askopenfilename(
            title="Abrir archivo", filetypes=[("Archivos JERS", "*.jers")]
        )
        if not loadedFile:
            return
        self.fileRute = loadedFile
        self.fileName = ntpath.basename(self.fileRute)
        self.fileName = self.fileName[:-5]
        self.fileEntry.delete(0, tk.END)
        self.fileEntry.insert(0, self.fileName)
        self.activate_text()

        loadedFile = open(loadedFile, "r")
        self.codeText.insert(tk.END, loadedFile.read())
        loadedFile.close()

    # Guarda el código en un archivo
    def save(self):
        if self.is_file_saved():
            return
        # Guardar como...
        if self.fileRute == "" or self.fileName != self.fileEntry.get():
            savedFile = tkinter.filedialog.asksaveasfilename(
                defaultextension=".*",
                title="Guardar archivo",
                filetypes=[("Archivo JERS", "*.jers")],
                initialfile=self.fileEntry.get(),
            )
            if not savedFile:
                return
            self.fileRute = savedFile
            self.fileName = ntpath.basename(self.fileRute)
            self.fileName = self.fileName[:-5]
            self.fileEntry.delete(0, tk.END)
            self.fileEntry.insert(0, self.fileName)

            savedFile = open(savedFile, "w")
            savedFile.write(self.codeText.get("1.0", "end-1c"))
            savedFile.close()

        # Guardar en la misma ruta
        else:
            savedFile = open(self.fileRute, "w")
            savedFile.write(self.codeText.get("1.0", "end-1c"))
            savedFile.close()

        self.log("Archivo guardado!!\n", type_msg="info")

    # Activa la zona de edición de texto para editar un archivo
    def activate_text(self):
        self.lineCanvas.pack(side=tk.LEFT, fill=tk.Y)
        self.codeText.config(state="normal")
        self.fileEntry.pack(padx=20, side=tk.LEFT, fill=tk.X, expand=1)
        self.codeText.delete("1.0", tk.END)
        self.line_update()

    # Mueve los widgets de codigo y lineas con la misma scrollbar
    def scroll_both(self, *args):
        self.codeText.yview(*args)
        self.lineCanvas.redraw()

    # Mueve la barra y ambos textos cuando se usa el scroll del mouse
    def on_text_scroll(self, *args):
        self.textScroll.set(*args)
        self.scroll_both("moveto", args[0])

    # Actualiza el widget con los numeros de las líneas
    def line_update(self, *args):
        self.codeText.tag_remove("error_line", 1.0, "end")
        self.lineCanvas.redraw()
        self.codeText.edit_modified(False)

    # Verifica si los cambios en el archivo estan guardados
    def is_file_saved(self):
        if not self.codeText.winfo_ismapped():
            return True
        try:
            checkFile = open(self.fileRute, "r")
            if self.codeText.get("1.0", "end-1c") == checkFile.read():
                checkFile.close()
                if self.fileName != self.fileEntry.get():
                    return False
                return True
        except:
            pass
        return False

    # Ofrece la opción de guardar el archivo antes de cerrar la aplicación
    def on_closing(self):
        if not self.is_file_saved() and self.codeText.get("1.0", "end-1c") != "":
            response = tkinter.messagebox.askyesno(
                "Archivo no guardado ", "¿Guardar archivo?"
            )
            if response == 1:
                self.save()
        root.destroy()

    # Oculta o muestra la salida
    def hide_show_log(self):
        if self.isShown:
            self.logText.grid_remove()
            self.outScroll.grid_remove()
            self.isShown = False
            self.showButton.config(text="Mostrar")
        else:
            self.logText.grid()
            self.outScroll.grid()
            self.isShown = True
            self.showButton.config(text="Ocultar")

    # Resalta una línea en el código
    def highlight(self, line):
        self.codeText.tag_add("error_line", str(line) + ".0", str(line + 1) + ".0")

    # Limpia la salida
    def clear_log(self):
        self.logText.config(state="normal")
        self.logText.delete("1.0", tk.END)
        self.logText.config(state="disabled")

    # Imprime el mensaje en la salida
    def log(self, msg, type_msg="normal"):
        self.logText.config(state="normal")
        self.logText.insert(tk.END, msg, type_msg)
        if self.lockVar.get() == 1:
            self.logText.see(tk.END)
        self.logText.config(state="disabled")

    # Retorna el texto para compilarlo
    def get_text(self):
        return self.codeText.get("1.0", "end-1c")

    # Compila el código
    def compile_code(self):
        comp.compiling(self)

    # Compila y ejecuta el código
    def compile_run(self):
        comp.compiling_running(self)


# Inicializa la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
