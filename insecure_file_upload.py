import os
import http.server
import cgi

# Configuración del directorio donde se almacenarán los archivos subidos
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Extensiones permitidas (de manera incorrecta, incluye archivos peligrosos)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'exe', 'php'}

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        """ Maneja la subida de archivos (sin validación adecuada) """
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
                        # Obtener el nombre del archivo y verificar la extensión (sin validación adecuada)
                        filename = file_item.filename
                        if '.' in filename:
                            # Guardar el archivo sin comprobar su contenido
                            filepath = os.path.join(UPLOAD_FOLDER, filename)
                            with open(filepath, 'wb') as f:
                                f.write(file_item.file.read())  # Guardamos el archivo

                            self.send_response(200)
                            self.send_header('Content-type', 'text/html')
                            self.end_headers()
                            self.wfile.write(b'File uploaded successfully!')
                        else:
                            self.send_response(400)
                            self.send_header('Content-type', 'text/html')
                            self.end_headers()
                            self.wfile.write(b'Invalid file extension!')
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