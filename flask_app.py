from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Lista para guardar nombres sin duplicados
nombres = []

# Página web que muestra los nombres
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Jugadores en el juego</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f2f2f2; padding: 20px; }
        h1 { color: #333; }
        ul { list-style-type: none; padding: 0; }
        li { background: #e0e0e0; margin: 5px 0; padding: 10px; border-radius: 8px; }
    </style>
</head>
<body>
    <h1>Jugadores conectados:</h1>
    <ul>
        {% for nombre in nombres %}
            <li>{{ nombre }}</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def mostrar_nombres():
    return render_template_string(html, nombres=nombres)

@app.route("/", methods=["POST"])
def recibir_nombre():
    data = request.get_json()
    nombre = data.get("username")
    if nombre and nombre not in nombres:
        nombres.append(nombre)
    return jsonify({"status": "ok", "nombres": nombres})

if __name__ == "__main__":
    app.run(debug=True)
