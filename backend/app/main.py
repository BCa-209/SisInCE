from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Consulta de Estudiantes. Ve a /docs para la documentación."}
