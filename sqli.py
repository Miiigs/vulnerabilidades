import sqlite3

def get_user_data(user_id):
    # Directly incorporating user input into SQL query (vulnerable to SQL Injection)
    conn = sqlite3.connect("database.db")
    
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"  # vulnerable to SQL injection
    cursor.execute(query)
    
    result = cursor.fetchall()
    conn.close()
    
    return result
