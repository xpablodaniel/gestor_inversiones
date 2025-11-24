# 💼 Gestor de Inversiones en Criptoactivos

Una herramienta en Python para registrar y gestionar transacciones de criptoactivos (compras y ventas) usando SQLite. Diseñada para uso local en Linux, permitiéndote mantener un registro detallado de todas tus operaciones con su costo en dólares y moneda local.

## 🎯 Propósito

Este proyecto nace de la necesidad de mantener un registro claro y organizado de transacciones de criptoactivos (compras y ventas), especialmente útil para:

- 📊 Seguimiento de operaciones en múltiples criptoactivos (BTC, ETH, ADA, etc.)
- 💵 Control de costos y tipo de cambio al momento de cada transacción
- 📈 Análisis histórico de compras y ventas
- 🧮 Base para cálculos impositivos y análisis de rentabilidad

## 🚀 Características

- ✨ Registro de transacciones (compras y ventas):
  - Criptoactivos: BTC, ETH, ADA, etc.
  - Tipo de operación: COMPRA o VENTA
  - Cantidad y precio unitario
  - Costo total (incluyendo comisiones)
  - Tipo de cambio del dólar al momento de la transacción
- 📋 Consulta de transacciones con formato tabular
- 🔍 Filtros avanzados (por activo, tipo de operación, rango de fechas)
- ✏️ Actualización de registros sin necesidad de borrar
- 🗑️ Gestión de registros (borrado de transacciones)
- 🔒 Almacenamiento local en SQLite
- 💻 Interfaz de línea de comandos intuitiva

## 📦 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tuusuario/gestor_inversiones.git
cd gestor_inversiones
```

2. Crea y activa un entorno virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
.\\venv\\Scripts\\activate  # En Windows
```

3. Instala el paquete en modo desarrollo:
```bash
pip install -e .
```

## 🎮 Uso

### Comandos Disponibles

El gestor cuenta con **5 comandos principales**:

| Comando | Descripción | Argumentos |
|---------|-------------|-----------|
| `registro` | Registrar nueva transacción (compra o venta) | `--activo`, `--operacion`, `--cantidad`, `--precio`, `--costo`, `--dolar`, `--fecha` (opt) |
| `consulta` | Consultar transacciones con filtros | `--activo` (opt), `--operacion` (opt), `--desde` (opt), `--hasta` (opt) |
| `actualizar` | Actualizar transacción existente | `--id` (req), más cualquier campo a modificar |
| `borrar` | Eliminar una transacción | `--id` (req) |
| `resumen` | Ver saldo por activo e inventario | Sin argumentos |

---

### Registrar una nueva transacción:
```bash
# Registrar una compra
python -m gestor_inversiones registro \
    --activo BTC \
    --operacion COMPRA \
    --cantidad 0.5 \
    --precio 45000 \
    --costo 22500 \
    --dolar 1050

# Registrar una venta
python -m gestor_inversiones registro \
    --activo BTC \
    --operacion VENTA \
    --cantidad 0.1 \
    --precio 46000 \
    --costo 4600 \
    --dolar 1050

# Registrar con fecha específica (para operaciones atrasadas)
python -m gestor_inversiones registro \
    --activo ETH --operacion COMPRA --cantidad 2 --precio 2500 --costo 5000 --dolar 1000 \
    --fecha 2025-11-15
```

### Consultar transacciones:
```bash
# Consultar todas las transacciones
python -m gestor_inversiones consulta

# Filtrar solo compras
python -m gestor_inversiones consulta --operacion COMPRA

# Filtrar solo ventas
python -m gestor_inversiones consulta --operacion VENTA

# Filtrar por activo específico
python -m gestor_inversiones consulta --activo BTC

# Filtrar por rango de fechas
python -m gestor_inversiones consulta --desde 2025-11-01 --hasta 2025-11-30

# Combinar múltiples filtros
python -m gestor_inversiones consulta --activo ETH --operacion COMPRA --desde 2025-11-01
```

### Actualizar una transacción:
```bash
# Actualizar el nombre del activo
python -m gestor_inversiones actualizar --id 1 --activo BTC

# Actualizar múltiples campos
python -m gestor_inversiones actualizar --id 1 --activo ETH --cantidad 2 --precio 2500

# Cambiar el tipo de operación
python -m gestor_inversiones actualizar --id 2 --operacion VENTA

# Actualizar la fecha
python -m gestor_inversiones actualizar --id 1 --fecha 2025-10-15
```

### Borrar una transacción:
```bash
python -m gestor_inversiones borrar --id 1
```

### Ver resumen de saldos (inventario):
```bash
# Mostrar saldo de cada activo y alertas sobre inventario negativo
python -m gestor_inversiones resumen

# Ejemplo de salida:
# ============================================================
# 📊 RESUMEN DE SALDOS POR ACTIVO
# ============================================================
# BTC      | Saldo:   0.40000000
# ETH      | Saldo:   2.00000000
# ============================================================
# ✅ Todos los saldos son válidos (sin inventarios negativos).
```

**Nota:** Si registras una venta superior a tu inventario, se mostrará una ⚠️ **alerta en rojo** indicando el desequilibrio.

## 🧱 Estructura del Proyecto

```
gestor_inversiones/
├── gestor_inversiones/
│   ├── __init__.py
│   ├── __main__.py       # Punto de entrada como módulo
│   ├── db.py            # Gestión de base de datos SQLite
│   ├── crud.py          # Operaciones CRUD
│   ├── utils.py         # Utilidades y validaciones
│   └── cli.py           # Interface de línea de comandos
├── data/                # Almacenamiento de la base de datos
│   └── .gitkeep
├── tests/              # Pruebas unitarias
│   ├── __init__.py
│   └── test_crud.py
├── setup.py           # Configuración del paquete
└── requirements.txt   # Dependencias del proyecto
```

## 📝 Próximas Características

- [ ] Exportación a CSV para análisis en Excel
- [ ] Cálculo de rendimientos y ganancias/pérdidas
- [x] Filtros por fecha y tipo de activo
- [ ] Gráficos de distribución de portfolio
- [ ] Respaldo automático de la base de datos

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría hacer.

## � Control de Versiones y GitHub

### Preparación Inicial del Repositorio

1. Crear un nuevo repositorio en GitHub (sin inicializar con README)

2. Configurar el `.gitignore` (ya incluido en el proyecto):
```
# Base de datos y archivos generados
data/*.db
__pycache__/
*.pyc

# Entorno virtual
venv/
env/

# Archivos de sistema
.DS_Store
Thumbs.db
```

3. Inicializar el repositorio local y vincularlo con GitHub:
```bash
# Inicializar repositorio Git local
git init

# Agregar todos los archivos excepto los ignorados
git add .

# Primer commit
git commit -m "Inicialización del proyecto gestor_inversiones"

# Agregar el repositorio remoto (reemplaza USERNAME y REPO)
git remote add origin https://github.com/USERNAME/REPO.git

# Subir el código al repositorio remoto
git branch -M main
git push -u origin main
```

### Flujo de Trabajo Diario

1. Antes de comenzar a trabajar:
```bash
# Obtener cambios del repositorio remoto
git pull origin main
```

2. Al hacer cambios:
```bash
# Ver estado de cambios
git status

# Agregar cambios (excluyendo la base de datos automáticamente)
git add .

# Crear commit con los cambios
git commit -m "Descripción de los cambios realizados"

# Subir cambios a GitHub
git push origin main
```

### ⚠️ Consideraciones Importantes

- La carpeta `data/` está en el repositorio pero su contenido está ignorado
- La base de datos (`*.db`) no se sube a GitHub por seguridad
- Cada desarrollador tendrá su propia base de datos local
- Los archivos `__pycache__` y `.pyc` se ignoran automáticamente
- El entorno virtual (`venv/`) debe crearse localmente y no subirse

### 🔄 Respaldo de la Base de Datos

Para mantener un respaldo de tus datos:

1. Exportar datos (próxima característica):
```bash
# Próximamente
python -m gestor_inversiones exportar --formato csv
```

2. Guardar el archivo CSV en una ubicación segura

3. Para restaurar en una nueva instalación:
```bash
# Próximamente
python -m gestor_inversiones importar --archivo respaldo.csv
```

## 🛠️ Solución a: "table transacciones has no column named operacion"

Si al ejecutar `registro` u otra operación recibes este error, significa que tu archivo de base de datos local fue creado con un esquema antiguo (sin la columna `operacion`) y el código actual espera esa columna.

Qué hice (solución aplicada en este repositorio):
- Añadí una comprobación y migración segura en `gestor_inversiones/db.py` — al abrir la base de datos el código ahora:
    - crea la tabla `transacciones` si **no** existe,
    - comprueba si la columna `operacion` está presente, y si falta la **añade** con ALTER TABLE y un valor por defecto `'COMPRA'`.

Por qué funcionó aquí pero pudo fallar en el repositorio de trabajo (`github.com/hotel23demayo/gestor_inversiones`):

1. Código desactualizado: si en el repo remoto no aplicaste (pull) los últimos cambios que contienen la migración, el proceso de arranque no intentará añadir la columna.
2. Ruta o archivo distinto: tu instalación en el trabajo puede usar otra ruta o nombre de fichero para la DB (ej. `data/inversiones.db` vs `data/otro.db`).
3. Permisos/lock: problemas de permisos o bloqueo (otro proceso usando el fichero) pueden impedir ALTER TABLE y entonces la migración falla silenciosamente.
4. Versiones de Python/SQLite: entornos diferentes pueden comportarse distinto (aunque ALTER TABLE ADD COLUMN normalmente es compatible, versiones antiguas de SQLite pueden limitar operaciones más complejas).

Pasos recomendados para reparar/manualizar en el repo del trabajo:

- Verifica que tu copia del código está actualizada (pull) y que `db.py` incluye la lógica de migración.
    ```bash
    git pull origin main
    ```
- Comprueba la estructura actual de la tabla en la máquina de trabajo:
    ```bash
    python3 - << 'PY'
    import sqlite3
    conn = sqlite3.connect('data/inversiones.db')
    print(list(conn.execute("PRAGMA table_info(transacciones);")))
    conn.close()
    PY
    ```
- Si falta `operacion`, respalda y aplica la migración manualmente (si no deseas borrar la DB):
    ```bash
    cp data/inversiones.db data/inversiones.db.bak
    sqlite3 data/inversiones.db "ALTER TABLE transacciones ADD COLUMN operacion TEXT DEFAULT 'COMPRA';"
    ```
- Alternativa (si no necesitas conservar datos): borrar la DB y dejar que el código la recree con el esquema correcto
    ```bash
    rm data/inversiones.db
    python3 -m gestor_inversiones registro --activo BTC --operacion COMPRA --cantidad 0.5 --precio 45000 --costo 22500 --dolar 1050
    ```

Recomendación de seguridad: siempre hacer una copia (`.bak`) antes de ejecutar ALTER TABLE en producción o en datos importantes.

## �📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.
