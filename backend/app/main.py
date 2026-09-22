from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.routers import estudiantes

# Crear tablas en la base de datos (útil para SQLite local)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Consulta de Estudiantes",
    description="API REST para consultas de información estudiantil",
    version="1.0.0"
)

import os

# Configuración CORS para entorno local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(estudiantes.router)

# Ruta absoluta a la carpeta frontend
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))

# Montar los archivos estáticos en la raíz (html=True para servir index.html)
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
