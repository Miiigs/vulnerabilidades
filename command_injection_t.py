import sqlite3
import subprocess

def get_user_data(username):
    # Conexión segura a la base de datos usando una consulta parametrizada
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    
    # Uso de una consulta parametrizada para evitar inyección SQL
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))

    try:
        user_data = cursor.fetchall()
    except sqlite3.DatabaseError as e:
        print(f"Error de base de datos: {e}")
        user_data = []
    finally:
        connection.close()

    # Ejecución segura sin invocar el shell directamente
    subprocess.run(["echo", username], check=True)

    # Escritura segura de los datos en un archivo
    with open("output.txt", "w") as f:
        f.write(str(user_data))
    
    return user_data