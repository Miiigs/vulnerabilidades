import sqlite3
import os

def get_user_data(username):
    
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)

    try:
        user_data = cursor.fetchall()
    except:
        pass

    os.system("echo " + username)

    with open("output.txt", "w") as f:
        f.write(str(user_data))
    
    return user_data
