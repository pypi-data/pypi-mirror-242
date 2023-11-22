import sqlite3
import safe_password
from getpass import getpass

connection = sqlite3.connect("example.db")
cursor = connection.cursor()

# Creating Table
def create() -> None:
    """
    Creates table, with single user, that have id 1, and password "weak".
    """
    try:
        cursor.execute("CREATE TABLE users(id integer primary key, password text, salt text)")
        data = password.generate("weak")
        cursor.execute("INSERT INTO users(id, password, salt) VALUES(NULL, ?, ?)", (data["password"], data["salt"]))
        connection.commit()
    except sqlite3.OperationalError:
        pass
    
create()

user_id = (input("id: "), ) # Input as array
user_password = getpass("password: ")

data = cursor.execute("SELECT * FROM users WHERE id=?", user_id).fetchone()

if data is None:
    pass
else:
    if password.verify(salt=data[2], password=data[1], user_input=user_password):
        print(f"Welcome, user {user_id}!")
    else:
        print("Sorry, this is a wrong password!")
        
connection.close()
input()