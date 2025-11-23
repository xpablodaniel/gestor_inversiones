import sqlite3
import os

def get_db_connection():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    db_path = os.path.join(data_dir, "inversiones.db")
    conn = sqlite3.connect(db_path)
    
    # Crear tabla si no existe
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            activo TEXT NOT NULL,
            operacion TEXT CHECK(operacion IN ('COMPRA', 'VENTA')) NOT NULL,
            cantidad REAL NOT NULL,
            precio_unitario REAL NOT NULL,
            costo_total REAL NOT NULL,
            dolar_cambio REAL NOT NULL
        )
    """)
    return conn
