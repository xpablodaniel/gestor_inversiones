from .db import get_db_connection
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
