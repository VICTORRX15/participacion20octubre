import sqlite3

def create_database():
    # Conexión a la base de datos
    conn = sqlite3.connect('restaurante.db')
    cursor = conn.cursor()

    # Crear tablas
    cursor.execute('''
        DROP TABLE PLATOS;
    ''')

    cursor.execute('''
        DROP TABLE MESAS;
    ''')
    cursor.execute('''
        DROP TABLE PEDIDOS;
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Platos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Mesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero INTEGER NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plato_id INTEGER,
            mesa_id INTEGER,
            cantidad INTEGER,
            fecha TEXT,
            FOREIGN KEY (plato_id) REFERENCES Platos(id),
            FOREIGN KEY (mesa_id) REFERENCES Mesas(id)
        )
    ''')

    # Insertar datos en Platos
    cursor.executemany('''
        INSERT INTO Platos (nombre, precio) VALUES (?, ?)
    ''', [
        ('Pasta Alfredo', 12.50),
        ('Pizza Margarita', 10.00),
        ('Hamburguesa', 8.00),
        ('Ensalada César', 7.00),
        ('Sopa de Tomate', 5.50)
    ])

    # Insertar datos en Mesas
    cursor.executemany('''
        INSERT INTO Mesas (numero) VALUES (?)
    ''', [(1,), (2,), (3,), (4,), (5,)])

    # Insertar datos en Pedidos
    cursor.executemany('''
        INSERT INTO Pedidos (plato_id, mesa_id, cantidad, fecha) VALUES (?, ?, ?, ?)
    ''', [
        (1, 1, 2, '2023-11-01'),
        (2, 2, 1, '2023-11-01'),
        (3, 3, 3, '2023-11-02'),
        (4, 4, 1, '2023-11-02'),
        (5, 5, 2, '2023-11-03')
    ])

    # Guardar cambios y cerrar la conexión
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    print("Base de datos creada y datos iniciales insertados.")
