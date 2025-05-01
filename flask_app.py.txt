from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Hola Mama</title>
        </head>
        <body>
            <h1>¡Bienvenido a tu primera página en Flask!</h1>
            <p>Este es un servidor local creado por Emanuel 😎</p>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
