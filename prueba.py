from flask import Flask, request, render_template_string

app = Flask(__name__)

# Página principal con formulario para comentarios
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Recibir el comentario del usuario sin sanitizar
        user_comment = request.form.get("comment")
        
        # Plantilla HTML que muestra el comentario del usuario
        template = f"""
        <html>
            <body>
                <h1>Comentarios</h1>
                <form method="POST">
                    <textarea name="comment" placeholder="Escribe tu comentario aquí..."></textarea><br>
                    <input type="submit" value="Enviar">
                </form>
                <p>Tu comentario: {user_comment}</p> <!-- Vulnerabilidad XSS aquí -->
            </body>
        </html>
        """
        return render_template_string(template)

    # Muestra el formulario vacío
    return """
    <html>
        <body>
            <h1>Comentarios</h1>
            <form method="POST">
                <textarea name="comment" placeholder="Escribe tu comentario aquí..."></textarea><br>
                <input type="submit" value="Enviar">
            </form>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
