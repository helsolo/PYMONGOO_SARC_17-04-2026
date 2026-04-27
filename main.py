
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
    # Verificar si el usuario está logueado
    if not session.get('usuario_id'):
        flash("Debes iniciar sesión primero.")
        return redirect(url_for("secion"))

    # Obtener las tareas del usuario
    usuario_id = session.get('usuario_id')
    tareas = gestor.obtener_tareas_usuario(usuario_id)

    return render_template("GestordeTareas.html", tareas=tareas)

@app.route("/secion", methods=["GET", "POST"])
def secion():
    if request.method == "POST":
        correo = request.form.get("correo", "").strip().lower()
        contrasena = request.form.get("contrasena", "")
        usuario = gestor.autenticar_usuario(correo, contrasena)
        if usuario:
            session["usuario_id"] = usuario["_id"]
            session["usuario_nombre"] = usuario.get("nombre")
            flash("¡Bienvenido!")
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
                flash("¡Cuenta creada exitosamente!")
                return redirect(url_for("secion"))
        flash("Error al crear cuenta. Verifica los datos.")
    return render_template("formulario.html")

@app.route("/crear_tarea", methods=["POST"])
def crear_tarea():
    # Verificar si el usuario está logueado
    if not session.get('usuario_id'):
        flash("Debes iniciar sesión primero.")
        return redirect(url_for("secion"))

    titulo = request.form.get("titulo", "").strip()
    descripcion = request.form.get("descripcion", "").strip()

    if titulo:
        usuario_id = session.get('usuario_id')
        tarea_id = gestor.crear_tarea(usuario_id, titulo, descripcion)
        if tarea_id:
            flash("¡Tarea creada!")
        else:
            flash("Error al crear la tarea.")
    else:
        flash("El título es obligatorio.")

    return redirect(url_for("Tareas"))

@app.route("/cambiar_estado/<tarea_id>", methods=["POST"])
def cambiar_estado(tarea_id):
    # Verificar si el usuario está logueado
    if not session.get('usuario_id'):
        flash("Debes iniciar sesión primero.")
        return redirect(url_for("secion"))

    nuevo_estado = request.form.get("estado", "completada")

    if gestor.actualizar_estado_tarea(tarea_id, nuevo_estado):
        flash("Estado actualizado.")
    else:
        flash("Error al actualizar el estado.")

    return redirect(url_for("Tareas"))

@app.route("/eliminar_tarea/<tarea_id>", methods=["POST"])
def eliminar_tarea(tarea_id):
    # Verificar si el usuario está logueado
    if not session.get('usuario_id'):
        flash("Debes iniciar sesión primero.")
        return redirect(url_for("secion"))

    if gestor.eliminar_tarea(tarea_id):
        flash("Tarea eliminada.")
    else:
        flash("Error al eliminar la tarea.")

    return redirect(url_for("Tareas"))

@app.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión.")
    return redirect(url_for("index"))

@app.route("/recuperar")
def Contraseña():
    return render_template("recuperar_contra.html")

if __name__ == "__main__":
    app.run(debug=True)
