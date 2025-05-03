import sqlite3
import json

connection = sqlite3.connect('Realno game/database_movements.db')
cursor = connection.cursor()

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS movement (
# move TEXT
# )
# ''')

# cursor.execute("INSERT INTO movement (move) VALUES (?)", (json.dumps(["Up", "Up"]),))
# cursor.execute("INSERT INTO movement (move) VALUES (?)", (json.dumps(["Down", "Down"]),))


connection.close()