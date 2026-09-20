import sqlite3
import os

def contar_generos():
    # Aseguramos la ruta correcta hacia data_base.db
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "data_base.db")
    
    # 1. Nos conectamos a la base de datos
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    
    # 2. Definimos y ejecutamos la consulta SQL
    consulta = """
        SELECT 
            genero, 
            COUNT(id_estudiante) AS total
        FROM estudiante
        GROUP BY genero
        ORDER BY total DESC;
    """
    cursor.execute(consulta)
    
    # 3. Obtenemos todos los resultados
    resultados = cursor.fetchall()
    
    # 4. Imprimimos los resultados de forma ordenada en la terminal
    print("\n=== RESUMEN DE ESTUDIANTES POR GÉNERO ===")
    
    total_general = 0
    for genero, cantidad in resultados:
        # fetchall() devuelve una lista de tuplas, por ejemplo: ('Masculino', 8500)
        print(f" > {genero}: {cantidad:,} estudiantes")
        total_general += cantidad
        
    print("-" * 40)
    print(f"   TOTAL REGISTROS: {total_general:,}")
    print("=========================================\n")
    
    # 5. Cerramos la conexión
    conexion.close()

if __name__ == "__main__":
    contar_generos()