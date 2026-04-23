
from flask import Flask, render_template, request, redirect, url_for, session, flash
from app import GestorTareas

app = Flask(__name__, template_folder="template")
app.secret_key = "devsecret123"

gestor = GestorTareas()

@app.route("/")
def index():
    return render_template("inicio.html")

@app.route("/Gestor")
def Tareas():
    return render_template("GestordeTareas.html")

@app.route("/secion", methods=["GET", "POST"])
def secion():
    if request.method == "POST":
        correo = request.form.get("correo", "").strip().lower()
        contrasena = request.form.get("contrasena", "")
        usuario = gestor.autenticar_usuario(correo, contrasena)
        if usuario:
            session["usuario_id"] = usuario["_id"]
            session["usuario_nombre"] = usuario.get("nombre")
            return redirect(url_for("index"))
        flash("Correo o contraseña incorrectos.")
    return render_template("inicio_secion.html")

@app.route("/cuenta", methods=["GET", "POST"])
def inisiar():
    if request.method == "POST":
        nombres = request.form.get("nombres", "").strip()
        apellido = request.form.get("apellido", "").strip()
        correo = request.form.get("correo", "").strip().lower()
        contrasena = request.form.get("contrasena", "")
        confirmar_contrasena = request.form.get("confirmar_contrasena", "")
        if contrasena == confirmar_contrasena:
            usuario_id = gestor.crear_usuario(nombres, apellido, correo, contrasena)
            if usuario_id:
                flash("Cuenta creada.")
                return redirect(url_for("sesion"))
        flash("Error al crear cuenta.")
    return render_template("formulario.html")

@app.route("/recuperar")
def Contraseña():
    return render_template("recuperar_contra.html")



if __name__ == "__main__":
    app.run(debug=True)
