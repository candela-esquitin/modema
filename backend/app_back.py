from flask import Flask,request, jsonify, session
from flask_cors import CORS
from db import get_connection


app = Flask(__name__)
app.secret_key = "una_clave_secreta_que_sólo_tú_conozcas"
app.config["SESSION_COOKIE_DOMAIN"] = "localhost"
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_NAME"] = "my_session"
app.config["SESSION_COOKIE_SECURE"] = False


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



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=True)