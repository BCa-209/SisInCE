from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/api/estudiantes",
    tags=["estudiantes"]
)

@router.get("/", response_model=List[schemas.Estudiante])
def get_estudiantes(
    nombre: Optional[str] = None,
    facultad: Optional[str] = None,
    escuela: Optional[str] = None,
    codigo: Optional[str] = None,
    dni: Optional[str] = None,
    ingreso: Optional[int] = None,
    ciclo: Optional[str] = None,
    genero: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Estudiante).outerjoin(models.Facultad).outerjoin(models.Escuela)
    
    if nombre:
        query = query.filter(
            or_(
                models.Estudiante.nombres.ilike(f"%{nombre}%"),
                models.Estudiante.apellido_paterno.ilike(f"%{nombre}%"),
                models.Estudiante.apellido_materno.ilike(f"%{nombre}%")
            )
        )
    if facultad:
        query = query.filter(models.Facultad.nombre.ilike(f"%{facultad}%"))
    if escuela:
        query = query.filter(models.Escuela.nombre.ilike(f"%{escuela}%"))
    if codigo:
        query = query.filter(models.Estudiante.codigo.ilike(f"%{codigo}%"))
    if dni:
        query = query.filter(models.Estudiante.dni.ilike(f"%{dni}%"))
    if ingreso is not None:
        query = query.filter(models.Estudiante.anio_ingreso == ingreso)
    if ciclo:
        query = query.filter(models.Estudiante.ciclo == ciclo) # Podría requerir casteo si ciclo es Int pero se pasa String
    if genero:
        query = query.filter(models.Estudiante.genero.ilike(genero))
        
    estudiantes = query.all()
    return estudiantes

@router.get("/facultades", response_model=List[schemas.Facultad])
def get_facultades(db: Session = Depends(get_db)):
    return db.query(models.Facultad).all()

@router.get("/escuelas", response_model=List[schemas.Escuela])
def get_escuelas(db: Session = Depends(get_db)):
    return db.query(models.Escuela).all()

@router.get("/codigo/{codigo}", response_model=schemas.Estudiante)
def get_estudiante_by_codigo(codigo: str, db: Session = Depends(get_db)):
    estudiante = db.query(models.Estudiante).filter(models.Estudiante.codigo == codigo).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante

@router.get("/dni/{dni}", response_model=schemas.Estudiante)
def get_estudiante_by_dni(dni: str, db: Session = Depends(get_db)):
    estudiante = db.query(models.Estudiante).filter(models.Estudiante.dni == dni).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante
