from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.session_db import get_session_db
from app.auth_service import validate_and_renew_session
from app import models

SESSION_COOKIE_NAME = "session_id"

def get_current_student(
    request: Request,
    db: Session = Depends(get_db),
    session_db: Session = Depends(get_session_db)
) -> models.Estudiante:
    """
    Dependencia de seguridad para FastAPI:
    1. Lee la cookie HttpOnly 'session_id'
    2. Comprueba que la sesión exista, no esté revocada y no haya expirado
    3. Renueva la sesión por 30 minutos de inactividad
    4. Recupera la entidad del estudiante de la base original (solo lectura)
    """
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado. Por favor inicie sesión."
        )

    sesion = validate_and_renew_session(session_db, token)
    if not sesion:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesión no válida o expirada. Inicie sesión nuevamente."
        )

    estudiante = db.query(models.Estudiante).filter(
        models.Estudiante.codigo == sesion.codigo_estudiante
    ).first()

    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no registrado en la base de datos."
        )

    return estudiante

