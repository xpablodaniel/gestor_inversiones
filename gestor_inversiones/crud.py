from .db import get_db_connection
import pandas as pd
from datetime import datetime

def registrar_transaccion(activo, operacion, cantidad, precio_unitario, costo_total, dolar_cambio, fecha=None):
    """Registra una transacción (compra o venta) en la base de datos.

    Parámetros:
    - activo: nombre del criptoactivo (ej: BTC, ETH)
    - operacion: tipo de operación ('COMPRA' o 'VENTA')
    - cantidad: cantidad en valores positivos (la operación define si suma o resta)
    - precio_unitario: precio por unidad en el momento de la transacción
    - costo_total: monto total de la transacción
    - dolar_cambio: tipo de cambio del dólar en ese momento
    - fecha: opcional. Si se indica, puede ser:
        * un objeto `datetime`
        * un string en formato ISO (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS)
      Si no se indica, la base de datos usará la fecha/hora actual.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    if fecha is None:
        cursor.execute("""
            INSERT INTO transacciones 
            (activo, operacion, cantidad, precio_unitario, costo_total, dolar_cambio)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (activo, operacion, cantidad, precio_unitario, costo_total, dolar_cambio))
    else:
        # Normalizar fecha a string
        if hasattr(fecha, 'isoformat'):
            fecha_str = fecha.isoformat(sep=' ')
        else:
            fecha_str = str(fecha)

        cursor.execute("""
            INSERT INTO transacciones 
            (fecha, activo, operacion, cantidad, precio_unitario, costo_total, dolar_cambio)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (fecha_str, activo, operacion, cantidad, precio_unitario, costo_total, dolar_cambio))

    conn.commit()
    conn.close()
    return True

# Mantener compatibilidad con nombre anterior
def registrar_compra(activo, operacion, cantidad, precio_unitario, costo_total, dolar_cambio, fecha=None):
    """Alias para registrar_transaccion (mantiene compatibilidad)."""
    return registrar_transaccion(activo, operacion, cantidad, precio_unitario, costo_total, dolar_cambio, fecha)

def consultar_registros(activo=None, operacion=None, fecha_desde=None, fecha_hasta=None):
    """Consulta registros de transacciones con filtros opcionales.
    
    Parámetros:
    - activo: filtrar por nombre de activo (ej: "BTC", "ETH")
    - operacion: filtrar por tipo de operación ("COMPRA", "VENTA")
    - fecha_desde: filtrar transacciones desde una fecha (formato ISO: YYYY-MM-DD)
    - fecha_hasta: filtrar transacciones hasta una fecha (formato ISO: YYYY-MM-DD)
    
    Retorna:
    - DataFrame con los registros que coinciden con los filtros
    """
    conn = get_db_connection()
    
    query = "SELECT * FROM transacciones WHERE 1=1"
    params = []
    
    # Agregar filtros dinámicamente
    if activo:
        query += " AND LOWER(activo) = LOWER(?)"
        params.append(activo)
    
    if operacion:
        query += " AND operacion = ?"
        params.append(operacion)
    
    if fecha_desde:
        query += " AND DATE(fecha) >= ?"
        params.append(fecha_desde)
    
    if fecha_hasta:
        query += " AND DATE(fecha) <= ?"
        params.append(fecha_hasta)
    
    query += " ORDER BY fecha DESC"
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def actualizar_transaccion(id_transaccion, **kwargs):
    """Actualiza uno o más campos de una transacción existente.
    
    Parámetros:
    - id_transaccion: ID del registro a actualizar
    - **kwargs: pares campo=valor a actualizar (activo, operacion, cantidad, precio_unitario, costo_total, dolar_cambio, fecha)
    
    Retorna:
    - True si se actualizó exitosamente
    - False si el registro no existe
    """
    if not kwargs:
        return False
    
    # Validar que los campos sean válidos
    campos_validos = {'activo', 'operacion', 'cantidad', 'precio_unitario', 'costo_total', 'dolar_cambio', 'fecha'}
    campos = set(kwargs.keys())
    
    campos_invalidos = campos - campos_validos
    if campos_invalidos:
        raise ValueError(f"Campos no válidos: {campos_invalidos}")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Construir dinámicamente la sentencia UPDATE
    set_clause = ", ".join([f"{campo} = ?" for campo in kwargs.keys()])
    values = list(kwargs.values())
    values.append(id_transaccion)
    
    query = f"UPDATE transacciones SET {set_clause} WHERE id = ?"
    cursor.execute(query, values)
    actualizado = cursor.rowcount > 0
    
    conn.commit()
    conn.close()
    return actualizado

def borrar_transaccion(id_transaccion):
    """Borra una transacción por ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM transacciones WHERE id = ?", (id_transaccion,))
    eliminado = cursor.rowcount > 0
    
    conn.commit()
    conn.close()
    return eliminado

def calcular_saldos():
    """Calcula el saldo de cada activo (COMPRA - VENTA) y detecta inventarios negativos.
    
    Retorna:
    - dict con estructura: {
        'saldos': {activo: cantidad_neta},
        'alertas': [lista de alertas sobre saldos negativos]
      }
    """
    conn = get_db_connection()
    
    # Consultar todas las transacciones agrupadas por activo y operación
    query = """
        SELECT activo, operacion, SUM(cantidad) as total
        FROM transacciones
        GROUP BY activo, operacion
        ORDER BY activo
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Calcular saldos netos
    saldos = {}
    alertas = []
    
    # Primero, agrupar por activo
    for activo in df['activo'].unique():
        df_activo = df[df['activo'] == activo]
        
        compras = df_activo[df_activo['operacion'] == 'COMPRA']['total'].sum()
        ventas = df_activo[df_activo['operacion'] == 'VENTA']['total'].sum()
        
        # Si hay NaN (no hay registros de ese tipo), asumir 0
        compras = compras if pd.notna(compras) else 0
        ventas = ventas if pd.notna(ventas) else 0
        
        saldo_neto = compras - ventas
        saldos[activo] = saldo_neto
        
        # Alertar si el saldo es negativo
        if saldo_neto < 0:
            alertas.append(
                f"⚠️ ALERTA: {activo} tiene saldo NEGATIVO: {saldo_neto:.8f}. "
                f"Compras: {compras:.8f}, Ventas: {ventas:.8f}"
            )
    
    return {
        'saldos': saldos,
        'alertas': alertas
    }
