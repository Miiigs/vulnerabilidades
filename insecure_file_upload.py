from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from PIL import Image
import magic

app = Flask(__name__)

# Ruta para la subida de archivos
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Extensiones permitidas, solo imágenes
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Límite de tamaño de archivo (en bytes)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Función para validar la extensión del archivo
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Función para validar el tipo de archivo mediante su contenido
def is_image(file):
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(file.read(1024))  # Leer solo los primeros 1024 bytes
    file.seek(0)  # Volver al inicio del archivo después de leer
    return file_type.startswith('image/')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        if not is_image(file):
            return jsonify({"error": "File is not a valid image"}), 400
        
        filename = secure_filename(file.filename)  # Asegura que el nombre del archivo sea seguro
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        file.save(filepath)
        return jsonify({"message": "File successfully uploaded"}), 200
    else:
        return jsonify({"error": "Invalid file extension"}), 400

if __name__ == '__main__':
    app.run(debug=True)