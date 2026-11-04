from pydantic import BaseModel, Field
from typing import Optional

class EstudianteBase(BaseModel):
    codigo: str
    apellidos_nombres: str
    dni: str
    facultad: str
    escuela_profesional: str
    anio_ingreso: Optional[int] = None
    ciclo: Optional[int] = None

class Estudiante(EstudianteBase):
    class Config:
        from_attributes = True

class FacultadBase(BaseModel):
    id_facultad: int
    nombre: str

class Facultad(FacultadBase):
    class Config:
        from_attributes = True

class EscuelaBase(BaseModel):
    id_escuela: int
    nombre: str
    id_facultad: Optional[int] = None

class Escuela(EscuelaBase):
    class Config:
        from_attributes = True

# --- Esquemas de Autenticación ---

class LoginRequest(BaseModel):
    nombres: str = Field(..., min_length=1, description="Nombres del estudiante")
    apellidos: str = Field(..., min_length=1, description="Apellidos (paterno y materno) del estudiante")
    codigo: str = Field(..., min_length=1, description="Código de estudiante")

class EstudianteAuthProfile(BaseModel):
    codigo: str
    nombres: str
    apellidos_nombres: str
    dni: Optional[str] = None
    facultad: str
    escuela_profesional: str
    anio_ingreso: Optional[int] = None
    ciclo: Optional[int] = None

    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    message: str
    estudiante: EstudianteAuthProfile

class MessageResponse(BaseModel):
    message: str
