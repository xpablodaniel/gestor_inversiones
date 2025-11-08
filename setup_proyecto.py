import os
import shutil

# Estructura de carpetas y archivos
estructura = {
    "gestor_inversiones": {  # Este es el paquete Python
        "__init__.py": "",
        "db.py": '''import sqlite3
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
            tipo TEXT CHECK(tipo IN ('CRYPTO', 'ETF')) NOT NULL,
            cantidad REAL NOT NULL,
            precio_unitario REAL NOT NULL,
            costo_total REAL NOT NULL,
            dolar_cambio REAL NOT NULL
        )
    """)
    return conn
''',
        "crud.py": '''from .db import get_db_connection
import pandas as pd
from datetime import datetime

def registrar_compra(activo, tipo, cantidad, precio_unitario, costo_total, dolar_cambio):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO transacciones 
        (activo, tipo, cantidad, precio_unitario, costo_total, dolar_cambio)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (activo, tipo, cantidad, precio_unitario, costo_total, dolar_cambio))
    
    conn.commit()
    conn.close()
    return True

def consultar_registros():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM transacciones", conn)
    conn.close()
    return df

def borrar_transaccion(id_transaccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM transacciones WHERE id = ?", (id_transaccion,))
    eliminado = cursor.rowcount > 0
    
    conn.commit()
    conn.close()
    return eliminado
''',
        "utils.py": "# Validaciones y helpers\n",
        "cli.py": '''import argparse
from .crud import registrar_compra, consultar_registros, borrar_transaccion

def main():
    parser = argparse.ArgumentParser(
        description="Gestor de inversiones doméstico (CRYPTO/ETF) con SQLite.",
        epilog="Ejecuta 'python -m gestor_inversiones <comando> -h' para ayuda específica."
    )
    subparsers = parser.add_subparsers(dest='comando', required=True)

    # Subcomando: registro
    parser_registro = subparsers.add_parser('registro', help='Registrar una nueva compra.')
    parser_registro.add_argument('--activo', required=True)
    parser_registro.add_argument('--tipo', required=True, choices=['CRYPTO', 'ETF'])
    parser_registro.add_argument('--cantidad', required=True, type=float)
    parser_registro.add_argument('--precio', dest='precio_unitario', required=True, type=float)
    parser_registro.add_argument('--costo', dest='costo_total', required=True, type=float)
    parser_registro.add_argument('--dolar', dest='dolar_cambio', required=True, type=float)

    # Subcomando: consulta
    parser_consulta = subparsers.add_parser('consulta', help='Consultar registros.')

    # Subcomando: borrar
    parser_borrar = subparsers.add_parser('borrar', help='Borrar una transacción.')
    parser_borrar.add_argument('--id', required=True, type=int)

    args = parser.parse_args()

    if args.comando == 'registro':
        registrar_compra(
            args.activo,
            args.tipo,
            args.cantidad,
            args.precio_unitario,
            args.costo_total,
            args.dolar_cambio
        )
        print("✅ Compra registrada exitosamente")

    elif args.comando == 'consulta':
        df = consultar_registros()
        if len(df) > 0:
            print("\nRegistros encontrados:")
            print(df.to_string(index=False))
        else:
            print("No hay registros en la base de datos.")

    elif args.comando == 'borrar':
        if borrar_transaccion(args.id):
            print(f"✅ Transacción {args.id} eliminada exitosamente")
        else:
            print(f"❌ No se encontró la transacción {args.id}")

if __name__ == "__main__":
    main()
'''
    },
    "data": {
        ".gitkeep": ""
    },
    "tests": {
        "__init__.py": "",
        "test_crud.py": '''import unittest
from gestor_inversiones.crud import registrar_compra, consultar_registros, borrar_transaccion

class TestCrud(unittest.TestCase):
    def test_registro_consulta(self):
        # Prueba de registro
        registrar_compra("BTC", "CRYPTO", 0.1, 35000, 3500, 1000)
        df = consultar_registros()
        self.assertGreater(len(df), 0)
        
        # Prueba de borrado
        ultimo_id = df.iloc[-1]['id']
        self.assertTrue(borrar_transaccion(ultimo_id))

if __name__ == '__main__':
    unittest.main()
'''
    },
    "__init__.py": "",  # Este es para hacer el directorio raíz un paquete Python
    ".gitignore": '''data/*.db
__pycache__/
*.pyc
''',
    "README.md": '''# Gestor de Inversiones Doméstico

Un gestor simple para llevar registro de inversiones en CRYPTO y ETFs.

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

Para registrar una compra:
```bash
python -m gestor_inversiones registro --activo BTC --tipo CRYPTO --cantidad 0.1 --precio 35000 --costo 3500 --dolar 1000
```

Para consultar registros:
```bash
python -m gestor_inversiones consulta
```

Para borrar una transacción:
```bash
python -m gestor_inversiones borrar --id 1
```
''',
    "requirements.txt": "pandas\nsqlite3\n",
    "__main__.py": '''from gestor_inversiones.cli import main

if __name__ == "__main__":
    main()
'''
}

def crear_estructura(base_path="."):
    # Primero limpiamos cualquier estructura existente
    if os.path.exists(base_path) and base_path != ".":
        shutil.rmtree(base_path)
    
    # Creamos la estructura desde cero
    for nombre, contenido in estructura.items():
        ruta = os.path.join(base_path, nombre)
        if isinstance(contenido, dict):
            os.makedirs(ruta, exist_ok=True)
            for archivo, texto in contenido.items():
                archivo_path = os.path.join(ruta, archivo)
                os.makedirs(os.path.dirname(archivo_path), exist_ok=True)
                with open(archivo_path, "w") as f:
                    f.write(texto)
        else:
            with open(ruta, "w") as f:
                f.write(contenido)

    print(f"✅ Proyecto creado en: {os.path.abspath(base_path)}")

if __name__ == "__main__":
    crear_estructura()
