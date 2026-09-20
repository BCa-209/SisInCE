import sqlite3
import os
import gender_guesser.detector as gender

def asignar_generos():
    # Aseguramos la ruta a la base de datos
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "data_base.db")
    
    print("Conectando a data_base.db...")
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    
    # Inicializamos el detector de género
    detector = gender.Detector(case_sensitive=False)
    
    # Obtenemos a todos los estudiantes (ID y Nombres completos)
    cursor.execute("SELECT id_estudiante, nombres FROM estudiante")
    estudiantes = cursor.fetchall()
    
    actualizaciones = []
    
    print(f"Analizando {len(estudiantes)} registros... Esto tomará unos segundos.")
    
    for id_estudiante, nombres_completos in estudiantes:
        # Extraemos solo el primer nombre (ej: de "Brayan Luis" sacamos "Brayan")
        primer_nombre = nombres_completos.strip().split()[0]
        
        # El detector requiere que la primera letra sea mayúscula (Capitalize)
        primer_nombre = primer_nombre.capitalize()
        
        # Adivinamos el género
        resultado = detector.get_gender(primer_nombre)
        
        # Mapeamos el resultado en inglés a español
        if resultado in ['male', 'mostly_male']:
            genero_final = 'Masculino'
        elif resultado in ['female', 'mostly_female']:
            genero_final = 'Femenino'
        else:
            # Para 'unknown' (desconocido) o 'andy' (andrógeno/unisex)
            genero_final = 'No especificado'
            
        actualizaciones.append((genero_final, id_estudiante))
    
    print("Guardando los géneros en la base de datos...")
    
    # Usamos executemany para actualizar los 20,000 registros de golpe (muy rápido)
    cursor.executemany("""
        UPDATE estudiante 
        SET genero = ? 
        WHERE id_estudiante = ?
    """, actualizaciones)
    
    conexion.commit()
    conexion.close()
    
    print("¡Asignación completada con éxito!")

if __name__ == "__main__":
    asignar_generos()