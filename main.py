
from flask import Flask, render_template

app = Flask(__name__, template_folder="template")

@app.route("/")
def index():
    return render_template("inicio.html")

@app.route("/Gestor")
def Tareas():
    return render_template("GestordeTareas.html")

@app.route("/sesion")
def secion():
    return render_template("inicio_secion.html")

@app.route("/cuenta")
def inisiar():
    return render_template("formulario.html")

@app.route("/recuperar")
def Contraseña():
    return render_template("recuperar_contra.html")



if __name__ == "__main__":
    app.run(debug=True)
