import sqlite3

def get_user_data(user_id):
    # Conexión a la base de datos
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    
    # Consulta parametrizada para evitar inyección SQL
    query = "SELECT * FROM users WHERE id = ?"  # nosec B608
    cursor.execute(query, (user_id,))

    # Recuperación de los datos del usuario
    user_data = cursor.fetchall()
    
    # Cierre de la conexión
    connection.close()
    
    return user_data