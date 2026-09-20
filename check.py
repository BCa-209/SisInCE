import sqlite3
c = sqlite3.connect('d:/_Consultas-Estudiantes/db/data_base.db').cursor()
c.execute("PRAGMA table_info(estudiantes)")
print(c.fetchall())
