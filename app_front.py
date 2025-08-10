from flask import Flask, render_template, url_for, request, redirect, flash, session, jsonify
import os
import requests
import threading
from flask_mail import Mail, Message
from collections import defaultdict

API_BASE = "http://localhost:5002"

app = Flask(__name__)

app.secret_key = "una_clave_secreta_que_sólo_tú_conozcas"

app.config["SESSION_COOKIE_DOMAIN"] = "localhost"
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

app.config["MAIL_DEFAULT_SENDER"] = "hana.sushi.ar@gmail.com"
app.config["MAIL_USERNAME"] = "hana.sushi.ar@gmail.com"
app.config["MAIL_PASSWORD"] = "ykyy nybo kevw albi"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False

mail = Mail(app)


def obtener_proyectos():
    response = requests.get(f"{API_BASE}/proyectos")
    if response.status_code == 200:
        return response.json()
    return None

@app.route('/guardar_sesion_frontend', methods=["POST"])
def guardar_sesion_frontend():
    data = request.get_json()
    if not data or "usuario" not in data:
        return jsonify({'error': 'faltan datos'}), 400
    session["usuario"] = data["usuario"]
    return jsonify({'mensaje' : 'sesion guardada en frontend'}), 200

def traer_usuario(id):
    response = requests.get(f'{API_BASE}/usuarios/{id}')
    if response.status_code == 200:
        return response.json()
    return None


def eliminar_proyecto(id):
    response = requests.post(f"{API_BASE}/proyectos/eliminar/{id}")
    if response.status_code == 200:
        return ({"exito": "Proyecto eliminado correctamente"})
    return None


@app.route("/usuario/<id>", methods=["GET", "POST"])
def usuario(id):
    usuario = session.get("usuario")
    if request.method == "POST":
        proyecto_id = request.form["proyecto_id"]
        accion = request.form["accion"]
        if accion == 'eliminar':
            eliminar_proyecto(proyecto_id)
    if not usuario:
        flash('Debes iniciar sesion para ingresar', 'warning')
        return redirect(url_for('index'))
    
    if usuario["id"] != int(id):
        flash('No tenes permiso para ver este perfil', 'warning')
        return redirect(url_for('index'))
    
    usuario_info = traer_usuario(id)
    proyectos = obtener_proyectos()
    print(usuario)
    print(getattr(usuario, 'id', None))
    return render_template(
        'usuario.html', 
        usuario_info = usuario_info, 
        usuario=usuario, 
        proyectos=proyectos
    )


@app.route('/agregar_proyecto', methods=["GET", "POST"])
def agregar_proyecto():
    usuario = session.get("usuario")
    if not usuario:
        flash('Debes ser empleado para acceder aqui', 'warning')
        return redirect(url_for("index"))
    
    if request.method == "POST":
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        img_principal = request.files.get('img_principal')
        img_sec1 = request.files.get('img_sec1')
        img_sec2 = request.files.get('img_sec2')

        if not titulo or not descripcion or not img_principal:
            flash('Complete todos los campos obligatorios', 'danger')
            return redirect(url_for('agregar_proyecto'))

        # Preparar archivo(s) para envío a backend
        files = {
            'img_principal': (img_principal.filename, img_principal.stream, img_principal.mimetype)
        }
        if img_sec1 and img_sec1.filename != '':
            files['img_sec1'] = (img_sec1.filename, img_sec1.stream, img_sec1.mimetype)
        if img_sec2 and img_sec2.filename != '':
            files['img_sec2'] = (img_sec2.filename, img_sec2.stream, img_sec2.mimetype)

        data = {
            'titulo': titulo,
            'descripcion': descripcion
        }

        response = requests.post(f"{API_BASE}/cargar_proyecto", data=data, files=files)

        if response.status_code == 201:
            flash("Proyecto agregado correctamente", "success")
            return redirect(url_for('agregar_proyecto'))
        else:
            flash("Error al agregar proyecto", "danger")
            return redirect(url_for('agregar_proyecto'))

    return render_template('agregar_proyecto.html')

@app.route("/usuario", methods=["GET"])
def user_redirect():
    usuario = session.get("usuario")
    if not usuario:
        flash('Debes ser empleado para acceder aqui', 'warning')
        return redirect(url_for("index"))
    return redirect(url_for("usuario", id=usuario["id"]))

@app.route('/')
def index():
    usuario = session.get("usuario")
    proyectos = obtener_proyectos()
    return render_template('index.html', usuario = usuario, proyectos = proyectos)

@app.route('/proyectos')
def proyectos():
    proyectos = obtener_proyectos()
    return render_template('proyectos.html', proyectos = proyectos)

def iniciar_sesion(email, contrasenia):
    response = requests.post(
        f"{API_BASE}/usuario/login", json={"email": email, "contrasenia":contrasenia}
    )
    if response.status_code == 200:
        return response.json().get("usuario")
    return None

@app.route("/login", methods=["GET", "POST"])
def login():
    usuario = session.get("usuario")
    if usuario:
        return redirect(url_for("usuario", id=usuario["id"]))
    if request.method == "POST":
        email = request.form["email"]
        contrasenia = request.form["contrasenia"]
        if not email or not contrasenia:
            flash('por favor complete todos los campos', 'danger')
            return redirect(url_for('login'))
        usuario = iniciar_sesion(email,contrasenia)
        if usuario:
            session["usuario"] = usuario
            return redirect(url_for('login'))
        else:
            flash("Email o contraseña incorrectos", "danger")
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.clear()
    flash('Sesion cerrada con exito, hasta luego!', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run("localhost", port=8082, debug=True)
