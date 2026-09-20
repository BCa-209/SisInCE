import sqlite3
import os

def migrar_base_de_datos():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CARPETA_RAIZ = os.path.dirname(BASE_DIR)
    
    DB_ORIGEN = os.path.join(CARPETA_RAIZ, "estudiantes.db")
    DB_DESTINO = os.path.join(BASE_DIR, "data_base.db")

    if not os.path.exists(DB_ORIGEN):
        print(f"Error: No se encontró el archivo original en {DB_ORIGEN}")
        return

    print("Conectando y creando data_base.db...")
    conexion = sqlite3.connect(DB_DESTINO)
    cursor = conexion.cursor()
    
    cursor.execute(f"ATTACH DATABASE '{DB_ORIGEN}' AS db_origen")

    # 1. Crear las nuevas tablas con la estructura actualizada (apellidos separados y doble llave foránea)
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS facultad (
            id_facultad INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(150) NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS escuela (
            id_escuela INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(150) NOT NULL,
            id_facultad INTEGER,  
            FOREIGN KEY (id_facultad) REFERENCES facultad(id_facultad)
        );

        CREATE TABLE IF NOT EXISTS estudiante (
            id_estudiante INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo VARCHAR(20) NOT NULL UNIQUE,
            dni VARCHAR(15) UNIQUE,       
            nombres VARCHAR(100) NOT NULL,
            apellido_paterno VARCHAR(50) NOT NULL,
            apellido_materno VARCHAR(50), 
            genero VARCHAR(15),           
            anio_ingreso INTEGER NOT NULL,
            ciclo INTEGER NOT NULL,
            id_facultad INTEGER NOT NULL,     
            id_escuela INTEGER,               
            FOREIGN KEY (id_facultad) REFERENCES facultad(id_facultad),
            FOREIGN KEY (id_escuela) REFERENCES escuela(id_escuela)
        );
    ''')

    # 2. Migrar Facultades
    cursor.execute('''
        INSERT OR IGNORE INTO facultad (nombre)
        SELECT DISTINCT facultad FROM db_origen.estudiantes WHERE facultad IS NOT NULL;
    ''')

    # 3. Migrar Escuelas
    cursor.execute('''
        INSERT OR IGNORE INTO escuela (nombre, id_facultad)
        SELECT DISTINCT orig.escuela, fac.id_facultad
        FROM db_origen.estudiantes orig
        LEFT JOIN facultad fac ON orig.facultad = fac.nombre
        WHERE orig.escuela IS NOT NULL;
    ''')

    # 4. Leer todos los estudiantes para procesar los apellidos en Python
    cursor.execute('''
        SELECT 
            CAST(orig.codigo AS VARCHAR) AS codigo,
            CAST(orig.dni AS VARCHAR) AS dni,
            orig.nombres,
            orig.apellidos,
            orig.facultad,
            orig.escuela,
            CAST(('20' || SUBSTR(CAST(orig.codigo AS VARCHAR), 1, 2)) AS INTEGER) AS anio_ingreso
        FROM db_origen.estudiantes orig;
    ''')
    
    estudiantes_crudos = cursor.fetchall()
    
    # Obtener diccionarios para mapear nombres de facultad/escuela a sus IDs
    cursor.execute("SELECT nombre, id_facultad FROM facultad")
    mapa_facultades = dict(cursor.fetchall())
    
    cursor.execute("SELECT nombre, id_escuela FROM escuela")
    mapa_escuelas = dict(cursor.fetchall())
    
    # 5. Procesar e insertar los estudiantes
    for est in estudiantes_crudos:
        codigo = est[0]
        dni = est[1]
        nombres = est[2]
        apellidos_completos = str(est[3] or "").strip()
        nombre_facultad = est[4]
        nombre_escuela = est[5]
        anio_ingreso = est[6]
        
        # --- Lógica para separar apellidos ---
        partes = apellidos_completos.split()
        apellido_paterno = ""
        apellido_materno = None
        
        if len(partes) >= 2:
            apellido_paterno = partes[0]
            # Unimos el resto como apellido materno (útil si hay apellidos compuestos)
            apellido_materno = " ".join(partes[1:])
        elif len(partes) == 1:
            apellido_paterno = partes[0]
        else:
            apellido_paterno = "Desconocido"
            
        id_facultad = mapa_facultades.get(nombre_facultad)
        id_escuela = mapa_escuelas.get(nombre_escuela)
        
        # Como tu diseño ahora exige que id_facultad en estudiante sea NOT NULL (obligatorio), 
        # necesitamos asegurarnos de que no esté vacío. Si el excel no lo tiene, intentamos inferirlo
        # de la escuela, o creamos un registro temporal.
        if id_facultad is None:
             cursor.execute("SELECT id_facultad FROM escuela WHERE id_escuela = ?", (id_escuela,))
             res = cursor.fetchone()
             if res and res[0] is not None:
                 id_facultad = res[0]
             else:
                 cursor.execute("INSERT OR IGNORE INTO facultad (nombre) VALUES ('Facultad Sin Asignar')")
                 cursor.execute("SELECT id_facultad FROM facultad WHERE nombre = 'Facultad Sin Asignar'")
                 id_facultad = cursor.fetchone()[0]

        # Insertar estudiante con los datos ya separados
        try:
            cursor.execute('''
                INSERT INTO estudiante 
                (codigo, dni, nombres, apellido_paterno, apellido_materno, genero, anio_ingreso, ciclo, id_facultad, id_escuela)
                VALUES (?, ?, ?, ?, ?, NULL, ?, 1, ?, ?)
            ''', (codigo, dni, nombres, apellido_paterno, apellido_materno, anio_ingreso, id_facultad, id_escuela))
        except sqlite3.IntegrityError:
            # Ignorar silenciosamente si ya existe el código (evita errores si ejecutas el script 2 veces)
            pass

    # 6. Guardar y desvincular
    conexion.commit()
    cursor.execute("DETACH DATABASE db_origen")
    conexion.close()
    
    print("¡Migración completada! Apellidos separados y relaciones establecidas correctamente.")

if __name__ == "__main__":
    migrar_base_de_datos()