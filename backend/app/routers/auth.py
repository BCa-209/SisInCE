import os
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.session_db import get_session_db
from app import models, schemas
from app.dependencies import get_current_student, SESSION_COOKIE_NAME
from app.auth_service import (
    verify_student_credentials,
    check_rate_limit,
    record_failed_attempt,
    reset_failed_attempts,
    create_student_session,
    revoke_student_session,
    SESSION_INACTIVITY_MINUTES
)

router = APIRouter(
    prefix="/api/auth",
    tags=["autenticacion"]
)

COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() in ("true", "1")
COOKIE_SAMESITE = os.getenv("COOKIE_SAMESITE", "lax")
MAX_AGE_SECONDS = SESSION_INACTIVITY_MINUTES * 60

def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "127.0.0.1"

@router.post("/login", response_model=schemas.LoginResponse)
def login(
    payload: schemas.LoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    session_db: Session = Depends(get_session_db)
):
    ip_address = get_client_ip(request)
    user_agent = request.headers.get("user-agent")

    # 1. Control de abuso y límite de intentos (Fase 8)
    is_blocked, remaining = check_rate_limit(session_db, ip_address)
    if is_blocked:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Demasiados intentos fallidos. Intente nuevamente en {remaining} segundos."
        )

    # 2. Consulta en la base de datos original (solo lectura)
    codigo_clean = payload.codigo.strip()
    estudiante = db.query(models.Estudiante).filter(
        models.Estudiante.codigo == codigo_clean
    ).first()

    # 3. Verificación de identidad con 3 campos (nombres, apellidos, código)
    if not estudiante or not verify_student_credentials(
        estudiante=estudiante,
        nombres=payload.nombres,
        apellidos=payload.apellidos,
        codigo=payload.codigo
    ):
        record_failed_attempt(session_db, ip_address)
        # Mensaje genérico de seguridad para no divulgar si el código existe
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas. Verifique nombres, apellidos y código."
        )

    # 4. Éxito: Reiniciar contador de intentos fallidos
    reset_failed_attempts(session_db, ip_address)

    # 5. Generación de identificador criptográfico y persistencia en base de sesiones
    raw_token = create_student_session(
        session_db=session_db,
        estudiante=estudiante,
        ip_address=ip_address,
        user_agent=user_agent
    )

    # 6. Envío de cookie HttpOnly segura (Fase 5)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=raw_token,
        max_age=MAX_AGE_SECONDS,
        expires=MAX_AGE_SECONDS,
        path="/",
        httponly=True,
        samesite=COOKIE_SAMESITE,
        secure=COOKIE_SECURE
    )

    return {
        "message": "Inicio de sesión exitoso",
        "estudiante": estudiante
    }

@router.post("/logout", response_model=schemas.MessageResponse)
def logout(
    request: Request,
    response: Response,
    session_db: Session = Depends(get_session_db)
):
    raw_token = request.cookies.get(SESSION_COOKIE_NAME)
    if raw_token:
        revoke_student_session(session_db, raw_token)

    # Eliminar cookie en el cliente
    response.delete_cookie(
        key=SESSION_COOKIE_NAME,
        path="/",
        httponly=True,
        samesite=COOKIE_SAMESITE,
        secure=COOKIE_SECURE
    )

    return {"message": "Sesión cerrada correctamente"}

@router.get("/me", response_model=schemas.EstudianteAuthProfile)
def get_current_user_profile(
    current_student: models.Estudiante = Depends(get_current_student)
):
    """Devuelve la información de la persona con sesión activa."""
    return current_student

