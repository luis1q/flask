from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect('datos.db')
    return conn


# Funciones para crear la base de datos, crear tablas y agregar datos
def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        fullname TEXT NOT NULL,
                        email TEXT NOT NULL,
                        password TEXT NOT NULL
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        fullname TEXT NOT NULL,
                        message TEXT NOT NULL,
                        created_at TEXT NOT NULL
                    )''')
    db.commit()

def create_user(username, fullname, email, password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO users (username, fullname, email, password)
                      VALUES (?, ?, ?, ?)''', (username, fullname, email, password))
    db.commit()

def create_message(username, message):
    db = get_db()
    cursor = db.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''SELECT fullname FROM users WHERE username=?''', (username,))
    fullname = cursor.fetchone()[0]
    cursor.execute('''INSERT INTO messages (username, fullname, message, created_at)
                      VALUES (?, ?, ?, ?)''', (username, fullname, message, created_at))
    db.commit()

# Funciones para obtener datos de la base de datos
def get_all_messages():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM messages''')
    messages = cursor.fetchall()
    return messages

def get_user_messages(username):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM messages WHERE username=?''', (username,))
    messages = cursor.fetchall()
    return messages

# Rutas de la aplicación
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    fullname = request.form['fullname']
    email = request.form['email']
    password = request.form['password']
    create_user(username, fullname, email, password)
    return jsonify({'message': 'Usuario registrado exitosamente!'})

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM users WHERE username=? AND password=?''', (username, password))
    user = cursor.fetchone()
    if user is None:
        return jsonify({'message': 'Nombre de usuario o contraseña incorrecta'})
    else:
        return jsonify({'message': 'Inicio de sesión exitoso!'})

@app.route('/messages', methods=['GET'])
def messages():
    messages = get_all_messages()
    return jsonify({'messages': messages})

@app.route('/messages/<username>', methods=['GET'])
def user_messages(username):
    messages = get_user_messages(username)
    return jsonify({'messages': messages})

@app.route('/messages', methods=['POST'])
def add_message():
    username = request.form['username']
    message = request.form['message']
    create_message(username, message)
    return jsonify({'message': 'Mensaje agregado exitosamente!'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
