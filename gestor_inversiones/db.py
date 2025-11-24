import sqlite3
import os

def get_db_connection():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    db_path = os.path.join(data_dir, "inversiones.db")
    conn = sqlite3.connect(db_path)
    
    # Crear tabla si no existe
    # Ensure table exists (idempotent)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            activo TEXT NOT NULL,
            operacion TEXT,
            cantidad REAL NOT NULL,
            precio_unitario REAL NOT NULL,
            costo_total REAL NOT NULL,
            dolar_cambio REAL NOT NULL
        )
    """)

    # Migration / safety: make sure 'operacion' column exists and has a sensible default
    # Older DBs might not have 'operacion' (or may have different column names). We'll
    # detect whether the column is present and, if missing, add it with a default value
    # so the rest of the code (which expects COMPRA/VENTA) doesn't crash.
    cur = conn.execute("PRAGMA table_info(transacciones);")
    cols = [row[1] for row in cur.fetchall()]
    if 'operacion' not in cols:
        # Add column with default 'COMPRA' for compatibility (ALTER TABLE adds the value
        # to existing rows). We avoid adding a CHECK constraint here to keep ALTER simple.
        try:
            conn.execute("ALTER TABLE transacciones ADD COLUMN operacion TEXT DEFAULT 'COMPRA';")
            conn.commit()
        except Exception:
            # If ALTER fails for any reason, just continue — the table exists but may be incompatible.
            # The rest of the app will raise informative errors later; user can choose to delete/backup DB.
            pass
    return conn
