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


@app.route('/')
def index():
    usuario = session.get("usuario")
    proyectos = obtener_proyectos()
    return render_template('index.html', usuario = usuario, proyectos = proyectos)

@app.route('/proyectos')
def proyectos():
    proyectos = obtener_proyectos()
    return render_template('proyectos.html', proyectos = proyectos)

@app.route('/usuario')
def usuario():
    return render_template('usuario.html')

if __name__ == '__main__':
    app.run(debug=True)
