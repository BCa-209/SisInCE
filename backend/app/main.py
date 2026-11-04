import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< Updated upstream
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.routers import estudiantes
=======
from app.session_db import init_session_db
from app.routers import estudiantes, auth
>>>>>>> Stashed changes

# Inicializar base de datos independiente de sesiones
init_session_db()

app = FastAPI(
    title="API Consulta de Estudiantes",
    description="API REST para consultas de información estudiantil con autenticación mediante sesiones seguras",
    version="1.1.0"
)

# Determinar los orígenes permitidos
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:8001")
origins = [
    frontend_url,
    "http://localhost:8001",
    "http://127.0.0.1:8001",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

# Configuración CORS para soporte de cookies de sesión HttpOnly
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(auth.router)
app.include_router(estudiantes.router)

<<<<<<< Updated upstream
# Ruta absoluta a la carpeta frontend
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))

# Montar los archivos estáticos en la raíz (html=True para servir index.html)
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
=======
@app.get("/")
def read_root():
    return {
        "message": "API de Consulta Estudiantil - Backend Funcionando",
        "auth": "Sesiones seguras HttpOnly activas (30 min inactividad)"
    }
>>>>>>> Stashed changes
