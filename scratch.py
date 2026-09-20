import sqlite3
conn = sqlite3.connect('db/data_base.db')
print("ESTUDIANTES:", conn.execute("PRAGMA table_info('estudiantes')").fetchall())
print("ESCUELA:", conn.execute("PRAGMA table_info('escuela')").fetchall())
print("ESTUDIANTE:", conn.execute("PRAGMA table_info('estudiante')").fetchall())
