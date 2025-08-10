from flask import Flask,request, jsonify, session
from flask_cors import CORS
from db import get_connection
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = "una_clave_secreta_que_sólo_tú_conozcas"
app.config["SESSION_COOKIE_DOMAIN"] = "localhost"
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_NAME"] = "my_session"
app.config["SESSION_COOKIE_SECURE"] = False

# Carpeta de destino -> static/images
UPLOAD_FOLDER = os.path.join(app.root_path, '..', 'static', 'images')
UPLOAD_FOLDER = os.path.abspath(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Extensiones permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


CORS(app, supports_credentials=True, origins=["http://localhost:8082"])

@app.route('/proyectos', methods=["GET"])
def obtener_proyectos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM proyectos
    """)

    proyectos = cursor.fetchall()

    return jsonify(proyectos), 200

@app.route('/proyectos/eliminar/<int:id>', methods=["POST"])
def eliminar_proyecto(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        DELETE FROM proyectos WHERE id=%s
    """, (id,))

    conn.commit()

    return ({"exito": "usuario borrado"}), 200


@app.route("/usuario")
def get_usuarios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(usuarios)

@app.route("/usuario/<int:id>", methods=["GET"])
def get_usuario(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    if not usuario:
        return ("Usuario no encontrado", 404)
    return jsonify(usuario)

@app.route("/usuario/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    contrasenia = data.get("contrasenia")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)
    cursor.execute("SELECT * FROM usuarios WHERE email= %s AND contrasenia = %s", (email,contrasenia,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    if usuario:
        session["logeado"] = True
        session["name"] = email
        return jsonify({"usuario": usuario}), 200
    else:
        return jsonify({"error": "Ususario o contraseña incorrectos"}), 401


@app.route("/usuario/index", methods=["GET"])
def usuario_logeado():
    if "logeado" in session and session["logeado"]:
        return jsonify ({"exito": "Ya estas logeado"}), 200
    else:
        return jsonify({"error": "No estas logeado"}), 401
    

def guardar_imagen(archivo):
    if archivo and allowed_file(archivo.filename):
        filename = secure_filename(archivo.filename)
        ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        archivo.save(ruta_archivo)
        # Devuelvo la ruta relativa para guardar en la DB
        return f'images/{filename}'
    return None


@app.route("/cargar_proyecto", methods=["POST"])
def cargar_proyecto():

    if 'img_principal' not in request.files:
        return jsonify({"error": "Imagen principal requerida"}), 400

    titulo = request.form.get("titulo")
    descripcion = request.form.get("descripcion")
    img_principal = request.files.get("img_principal")
    img_sec1 = request.files.get("img_sec1")
    img_sec2 = request.files.get("img_sec2")

    path_img_principal = guardar_imagen(img_principal)
    path_img_sec1 = guardar_imagen(img_sec1)
    path_img_sec2 = guardar_imagen(img_sec2)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO proyectos (titulo, descrip, img_principal, img_sec1, img_sec2)
        VALUES (%s, %s, %s, %s, %s)
    """, (titulo, descripcion, path_img_principal, path_img_sec1, path_img_sec2))
    conn.commit()
    cursor.close()
    conn.close()

    return {"mensaje": "Proyecto agregado correctamente"}, 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=True)