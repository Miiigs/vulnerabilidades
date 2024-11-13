import os
import http.server
import cgi
from werkzeug.utils import secure_filename
import magic

# Configuración del directorio donde se almacenarán los archivos subidos
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Extensiones permitidas para imágenes (de forma segura, solo imágenes)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Límite de tamaño de archivo (en bytes) - 5 MB por ejemplo
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

# Función para validar la extensión del archivo
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Función para validar el tipo MIME del archivo (contenido)
def is_image(file):
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(file.read(1024))  # Leer solo los primeros 1024 bytes
    file.seek(0)  # Volver al inicio del archivo después de leer
    return file_type.startswith('image/')

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        """ Maneja la subida de archivos con validaciones sanitizadas """
        if self.path == '/upload':
            # Recibir la información del formulario
            content_type, pdict = cgi.parse_header(self.headers['Content-Type'])
            if content_type == 'multipart/form-data':
                # Extraemos los campos del formulario (archivos y datos)
                form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})

                # Verificar si existe el archivo
                if 'file' in form:
                    file_item = form['file']
                    if file_item.filename:
                        # Obtener el nombre del archivo y verificar la extensión
                        filename = file_item.filename
                        if not allowed_file(filename):
                            self.send_response(400)
                            self.send_header('Content-type', 'text/html')
                            self.end_headers()
                            self.wfile.write(b'Invalid file extension!')
                            return

                        # Verificar el tamaño del archivo
                        if len(file_item.file.read()) > MAX_FILE_SIZE:
                            self.send_response(400)
                            self.send_header('Content-type', 'text/html')
                            self.end_headers()
                            self.wfile.write(b'File too large!')
                            return

                        # Rehacer el seek después de leer para comprobar el contenido
                        file_item.file.seek(0)
                        
                        # Validar que el archivo sea una imagen real por su contenido
                        if not is_image(file_item.file):
                            self.send_response(400)
                            self.send_header('Content-type', 'text/html')
                            self.end_headers()
                            self.wfile.write(b'File is not a valid image!')
                            return

                        # Hacer que el nombre del archivo sea seguro
                        safe_filename = secure_filename(filename)

                        # Ruta de destino para el archivo
                        filepath = os.path.join(UPLOAD_FOLDER, safe_filename)
                        
                        # Guardar el archivo de manera segura
                        with open(filepath, 'wb') as f:
                            f.write(file_item.file.read())

                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(b'File uploaded successfully!')
                    else:
                        self.send_response(400)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(b'No file selected!')
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'No file part in the request!')
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Invalid content type!')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Not Found')

def run(server_class=http.server.HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()