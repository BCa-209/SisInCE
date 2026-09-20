from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Facultad(Base):
    __tablename__ = "facultad"
    id_facultad = Column(Integer, primary_key=True)
    nombre = Column(String(150))

class Escuela(Base):
    __tablename__ = "escuela"
    id_escuela = Column(Integer, primary_key=True)
    nombre = Column(String(150))
    id_facultad = Column(Integer, ForeignKey("facultad.id_facultad"))
    
    facultad_rel = relationship("Facultad")

class Estudiante(Base):
    __tablename__ = "estudiante"
    id_estudiante = Column(Integer, primary_key=True)
    codigo = Column(String(20))
    dni = Column(String(15))
    nombres = Column(String(100))
    apellido_paterno = Column(String(50), nullable=False)
    apellido_materno = Column(String(50))
    genero = Column(String(15))
    anio_ingreso = Column(Integer)
    ciclo = Column(Integer)
    id_facultad = Column(Integer, ForeignKey("facultad.id_facultad"))
    id_escuela = Column(Integer, ForeignKey("escuela.id_escuela"))
    
    facultad_rel = relationship("Facultad")
    escuela_rel = relationship("Escuela")

    @property
    def apellidos_nombres(self):
        apellidos = f"{self.apellido_paterno or ''} {self.apellido_materno or ''}".strip()
        return f"{apellidos} {self.nombres or ''}".strip()

    @property
    def facultad(self):
        if self.facultad_rel:
            return self.facultad_rel.nombre
        return "No Registrado"

    @property
    def escuela_profesional(self):
        if self.escuela_rel:
            return self.escuela_rel.nombre
        return "No Registrado"
