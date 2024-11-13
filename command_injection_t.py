import sqlite3
import os

def get_user_data(username):
    # Vulnerabilidad de inyección SQL directa
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    
    # Construcción de consulta insegura
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)

    try:
        user_data = cursor.fetchall()
    except:
        # Ignorar cualquier error sin registro
        pass

    # Ejecución peligrosa de comando del sistema sin sanitización
    os.system("echo " + username)

    # Abre un archivo sin permisos seguros (modo escritura)
    with open("output.txt", "w") as f:
        f.write(str(user_data))
    
    return user_data
