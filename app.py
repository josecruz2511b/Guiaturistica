from flask import Flask, render_template, request, redirect, url_for, session, flash
import pyodbc
from config import Config

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = pyodbc.connect(Config.CONNECTION_STRING)
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Usuarios')
    usuarios = cursor.fetchall()
    conn.close()
    return render_template('index.html', usuarios=usuarios)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Usuarios WHERE correo = ? AND contraseña = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Credenciales inválidas. Por favor, inténtalo de nuevo.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Usuarios (nombre, apellido, correo, contraseña, fecha_registro) VALUES (?, ?, ?, ?, GETDATE())',
                       (nombre, apellido, correo, contraseña))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id_usuario>', methods=['GET', 'POST'])
def edit(id_usuario):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Usuarios WHERE id_usuario = ?', (id_usuario,))
    usuario = cursor.fetchone()
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        cursor.execute('UPDATE Usuarios SET nombre = ?, apellido = ?, correo = ?, contraseña = ? WHERE id_usuario = ?',
                       (nombre, apellido, correo, contraseña, id_usuario))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    conn.close()
    return render_template('edit.html', usuario=usuario)

@app.route('/delete/<int:id_usuario>', methods=['POST'])
def delete(id_usuario):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Usuarios WHERE id_usuario = ?', (id_usuario,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/administradores')
def administradores():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Administradores INNER JOIN Usuarios ON Administradores.id_usuario = Usuarios.id_usuario')
    administradores = cursor.fetchall()
    conn.close()
    return render_template('administradores.html', administradores=administradores)



@app.route('/add_administrador', methods=['GET', 'POST'])
def add_administrador():
    if request.method == 'POST':
        id_usuario = request.form['id_usuario']
        rol = request.form['rol']
        fecha_inicio = request.form['fecha_inicio']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Administradores (id_usuario, rol, fecha_inicio) VALUES (?, ?, ?)',
                       (id_usuario, rol, fecha_inicio))
        conn.commit()
        conn.close()

        flash('Administrador agregado correctamente', 'success')
        return redirect(url_for('administradores'))
    return render_template('add_administrador.html')


@app.route('/destinos')
def destinos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Destinos')
    destinos = cursor.fetchall()
    conn.close()
    return render_template('destinos.html', destinos=destinos)


@app.route('/add_destino', methods=['GET', 'POST'])
def add_destino():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        ubicacion = request.form['ubicacion']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Destinos (nombre, descripcion, ubicacion) VALUES (?, ?, ?)',
                       (nombre, descripcion, ubicacion))
        conn.commit()
        conn.close()

        flash('Destino agregado correctamente', 'success')
        return redirect(url_for('destinos'))
    return render_template('add_destino.html')



if __name__ == '__main__':
    app.run(debug=True)