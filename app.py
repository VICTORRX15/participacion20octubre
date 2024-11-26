from flask import Flask, render_template, request, g
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = 'restaurante.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Ruta para ver los platos
@app.route('/platos')
def platos():
    db = get_db()
    cur = db.execute('SELECT * FROM Platos')
    platos = cur.fetchall()
    return render_template('platos.html', platos=platos)

# Ruta para ver las mesas
@app.route('/mesas')
def mesas():
    db = get_db()
    cur = db.execute('SELECT * FROM Mesas')
    mesas = cur.fetchall()
    return render_template('mesas.html', mesas=mesas)

# Ruta para ver los pedidos
@app.route('/')
def pedidos():
    db = get_db()
    cur = db.execute('''
        SELECT Pedidos.id, Platos.nombre, Mesas.numero, Pedidos.cantidad, Pedidos.fecha 
        FROM Pedidos
        JOIN Platos ON Pedidos.plato_id = Platos.id
        JOIN Mesas ON Pedidos.mesa_id = Mesas.id
    ''')
    pedidos = cur.fetchall()
    return render_template('index.html', pedidos=pedidos)

# Ruta para agregar un pedido
@app.route('/agregar_pedido', methods=['GET', 'POST'])
def agregar_pedido():
    db = get_db()
    if request.method == 'POST':
        plato_id = request.form['plato_id']
        mesa_id = request.form['mesa_id']
        cantidad = request.form['cantidad']
        fecha = datetime.now().strftime('%Y-%m-%d')
        
        db.execute('INSERT INTO Pedidos (plato_id, mesa_id, cantidad, fecha) VALUES (?, ?, ?, ?)',
                   (plato_id, mesa_id, cantidad, fecha))
        db.commit()

        cur = db.execute('''
        SELECT Pedidos.id, Platos.nombre, Mesas.numero, Pedidos.cantidad, Pedidos.fecha 
        FROM Pedidos
        JOIN Platos ON Pedidos.plato_id = Platos.id
        JOIN Mesas ON Pedidos.mesa_id = Mesas.id
        ''')
        pedidos = cur.fetchall()
        return render_template('index.html',pedidos=pedidos)

    # Obtener los platos y mesas para mostrar en el formulario
    cur = db.execute('SELECT id, nombre FROM Platos')
    platos = cur.fetchall()
    cur = db.execute('SELECT id, numero FROM Mesas')
    mesas = cur.fetchall()
    return render_template('agregar_pedido.html', platos=platos, mesas=mesas)

if __name__ == '__main__':
    app.run(debug=True)
