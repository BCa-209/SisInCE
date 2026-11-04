
import sqlite3

# Base de datos original
BD_ORIGINAL = "data_base.db"

# Nueva base de datos
BD_NUEVA = "estudiantes_extraidos.db"

try:
    # Conectar a la base de datos original
    conexion_origen = sqlite3.connect(BD_ORIGINAL)
    cursor_origen = conexion_origen.cursor()

    # Extraer los datos de la tabla estudiante
    cursor_origen.execute("""
        SELECT
            id_estudiante,
            nombres,
            apellido_paterno,
            apellido_materno
        FROM estudiante
    """)

    registros = cursor_origen.fetchall()

    # Crear nueva base de datos
    conexion_nueva = sqlite3.connect(BD_NUEVA)
    cursor_nueva = conexion_nueva.cursor()

    # Crear tabla estudiante
    cursor_nueva.execute("""
        CREATE TABLE estudiante (
            id_estudiante INTEGER PRIMARY KEY,
            nombres TEXT,
            apellido_paterno TEXT,
            apellido_materno TEXT
        )
    """)

    # Insertar registros extraídos
    cursor_nueva.executemany("""
        INSERT INTO estudiante (
            id_estudiante,
            nombres,
            apellido_paterno,
            apellido_materno
        )
        VALUES (?, ?, ?, ?)
    """, registros)

    # Guardar cambios
    conexion_nueva.commit()

    print("¡Extracción realizada correctamente!")
    print(f"Registros extraídos: {len(registros)}")
    print(f"Archivo generado: {BD_NUEVA}")

except sqlite3.Error as e:
    print("Error durante la extracción:", e)

finally:
    if 'conexion_origen' in locals():
        conexion_origen.close()

    if 'conexion_nueva' in locals():
        conexion_nueva.close()
