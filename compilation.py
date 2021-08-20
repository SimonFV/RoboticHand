# Cuerpo de la compilación del código
def compiling(app):
    app.log("Compilando!!\n", type_msg="info")
    app.log("Error!!\n", type_msg="error")
    app.log("Warning!!\n", type_msg="warning")
    app.log("Saved!!\n", type_msg="info")


# Cuerpo de la compilación y ejecución del código
def compiling_running(app):
    app.log("Compilando y ejecutando!!\n", type_msg="success")
