from flask import Flask, request, render_template_string
import sqlite3
from datetime import datetime
import requests

app = Flask(__name__)

# Crear tabla si no existe
def crear_tabla():
    conn = sqlite3.connect("jugadores.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jugadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            equipo TEXT,
            fecha_hora TEXT,
            ip TEXT,
            pais TEXT
        )
    ''')
    conn.commit()
    conn.close()

crear_tabla()

# Función para obtener país por IP
def obtener_pais(ip):
    try:
        if ip == "127.0.0.1":
            return "Localhost"
        respuesta = requests.get(f"https://ipapi.co/{ip}/country_name/")
        if respuesta.status_code == 200:
            return respuesta.text.strip()
    except:
        return "Desconocido"
    return "Desconocido"

# Ruta principal
@app.route("/")
def inicio():
    conn = sqlite3.connect("jugadores.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, equipo, fecha_hora, pais FROM jugadores ORDER BY fecha_hora DESC")
    registros = cursor.fetchall()
    conn.close()

    html = """
    <h1>Historial de Jugadores</h1>
    <table border="1" cellpadding="5">
        <tr><th>Jugador</th><th>Equipo</th><th>Fecha y Hora</th><th>País</th></tr>
        {% for jugador in registros %}
        <tr>
            <td>{{ jugador[0] }}</td>
            <td>{{ jugador[1] }}</td>
            <td>{{ jugador[2] }}</td>
            <td>{{ jugador[3] }}</td>
        </tr>
        {% endfor %}
    </table>
    """
    return render_template_string(html, registros=registros)

# Ruta para recibir datos de Roblox
@app.route("/registrar", methods=["POST"])
def registrar():
    data = request.json
    username = data.get("username")
    equipo = data.get("equipo", "Desconocido")
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = request.remote_addr
    pais = obtener_pais(ip)

    conn = sqlite3.connect("jugadores.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jugadores (username, equipo, fecha_hora, ip, pais) VALUES (?, ?, ?, ?, ?)",
                   (username, equipo, fecha_hora, ip, pais))
    conn.commit()
    conn.close()

    return {"estado": "registrado", "fecha_hora": fecha_hora, "pais": pais}, 200

