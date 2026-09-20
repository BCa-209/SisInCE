from pydantic import BaseModel
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
        orm_mode = True
        from_attributes = True

class FacultadBase(BaseModel):
    id_facultad: int
    nombre: str

class Facultad(FacultadBase):
    class Config:
        orm_mode = True
        from_attributes = True

class EscuelaBase(BaseModel):
    id_escuela: int
    nombre: str
    id_facultad: Optional[int] = None

class Escuela(EscuelaBase):
    class Config:
        orm_mode = True
        from_attributes = True
