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

# Determinar los orígenes permitidos
# En producción, configurar la variable FRONTEND_URL con el dominio de Vercel
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:8001")
origins = [
    frontend_url,
    "http://localhost:8001",
    "http://127.0.0.1:8001"
]

# Configuración CORS para producción/Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(estudiantes.router)

# Ruta absoluta a la carpeta frontend
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))

# Montar los archivos estáticos en la raíz (html=True para servir index.html)
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
