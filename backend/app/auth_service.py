import secrets
import hashlib
import unicodedata
import re
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.session_db import Sesion, IntentoLogin

# Duración de inactividad de sesión: 30 minutos
SESSION_INACTIVITY_MINUTES = 30
# Límite de intentos fallidos antes de bloqueo temporal
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_MINUTES = 5

def normalize_text(text: str | None) -> str:
    """
    Normaliza texto removiendo acentos, signos de puntuación,
    convirtiendo a minúsculas y colapsando espacios múltiples.
    """
    if not text:
        return ""
    # Descomponer caracteres con acentos
    text = unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("utf-8")
    # Mantener sólo alfanuméricos y espacios
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    # Colapsar espacios y minúsculas
    return re.sub(r"\s+", " ", text).strip().lower()

def verify_student_credentials(estudiante, nombres: str, apellidos: str, codigo: str) -> bool:
    """
    Verifica los 3 campos de acceso:
    1. Código exacto (normalizado)
    2. Nombres (normalizados sin tildes ni mayúsculas)
    3. Apellidos (paterno y materno normalizados)
    """
    if not estudiante:
        return False

    # 1. Comprobación del código
    if normalize_text(estudiante.codigo) != normalize_text(codigo):
        return False

    # 2. Comprobación de los nombres
    norm_db_names = normalize_text(estudiante.nombres)
    norm_in_names = normalize_text(nombres)
    if norm_db_names != norm_in_names:
        return False

    # 3. Comprobación de apellidos
    paterno = estudiante.apellido_paterno or ""
    materno = estudiante.apellido_materno or ""
    full_db_apellidos = f"{paterno} {materno}".strip()

    norm_db_apellidos = normalize_text(full_db_apellidos)
    norm_in_apellidos = normalize_text(apellidos)

    if norm_db_apellidos == norm_in_apellidos:
        return True

    # Comparación por conjunto de palabras (para contemplar orden de apellidos)
    db_words = set(norm_db_apellidos.split())
    in_words = set(norm_in_apellidos.split())
    if db_words and db_words == in_words:
        return True

    # Si en la base de datos no hay materno o solo coincide el paterno único
    if not materno and normalize_text(paterno) == norm_in_apellidos:
        return True

    return False

def hash_session_token(token: str) -> str:
    """Devuelve el resumen SHA-256 del token."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()

def check_rate_limit(session_db: Session, ip_address: str) -> tuple[bool, int]:
    """
    Verifica si la IP está bloqueada por exceso de intentos fallidos.
    Retorna (is_blocked, remaining_seconds).
    """
    if not ip_address:
        return False, 0

    now = datetime.now(timezone.utc)
    attempt = session_db.query(IntentoLogin).filter(IntentoLogin.ip_address == ip_address).first()
    if not attempt:
        return False, 0

    # Manejar fechas con/sin timezone de SQLite
    blocked_until = attempt.blocked_until
    if blocked_until:
        if blocked_until.tzinfo is None:
            blocked_until = blocked_until.replace(tzinfo=timezone.utc)
        if blocked_until > now:
            remaining = int((blocked_until - now).total_seconds())
            return True, remaining
        else:
            # Desbloqueado: reiniciar contador
            attempt.failed_count = 0
            attempt.blocked_until = None
            session_db.commit()

    return False, 0

def record_failed_attempt(session_db: Session, ip_address: str) -> None:
    """Registra un intento fallido y bloquea si supera el umbral."""
    if not ip_address:
        return

    now = datetime.now(timezone.utc)
    attempt = session_db.query(IntentoLogin).filter(IntentoLogin.ip_address == ip_address).first()
    if not attempt:
        attempt = IntentoLogin(
            ip_address=ip_address,
            failed_count=1,
            last_failed_at=now,
            blocked_until=None
        )
        session_db.add(attempt)
    else:
        attempt.failed_count += 1
        attempt.last_failed_at = now
        if attempt.failed_count >= MAX_FAILED_ATTEMPTS:
            attempt.blocked_until = now + timedelta(minutes=LOCKOUT_MINUTES)
    session_db.commit()

def reset_failed_attempts(session_db: Session, ip_address: str) -> None:
    """Reinicia el contador de intentos fallidos tras login exitoso."""
    if not ip_address:
        return

    attempt = session_db.query(IntentoLogin).filter(IntentoLogin.ip_address == ip_address).first()
    if attempt:
        attempt.failed_count = 0
        attempt.blocked_until = None
        session_db.commit()

def create_student_session(
    session_db: Session,
    estudiante,
    ip_address: str | None = None,
    user_agent: str | None = None
) -> str:
    """
    Crea una sesión temporal independiente:
    - Genera token aleatorio criptográficamente seguro
    - Almacena sólo el hash en la base de datos de sesiones
    - Establece vencimiento de inactividad en 30 minutos
    - Retorna el token crudo para la cookie HttpOnly
    """
    now = datetime.now(timezone.utc)
    raw_token = secrets.token_urlsafe(48)
    token_hash = hash_session_token(raw_token)
    expires_at = now + timedelta(minutes=SESSION_INACTIVITY_MINUTES)

    sesion = Sesion(
        token_hash=token_hash,
        codigo_estudiante=estudiante.codigo,
        id_estudiante=getattr(estudiante, "id_estudiante", None),
        created_at=now,
        last_activity=now,
        expires_at=expires_at,
        revoked=False,
        ip_address=ip_address,
        user_agent=user_agent
    )
    session_db.add(sesion)
    session_db.commit()

    return raw_token

def validate_and_renew_session(session_db: Session, raw_token: str | None) -> Sesion | None:
    """
    Valida la sesión mediante el hash del token:
    1. Si no existe, venció o fue revocada -> Retorna None
    2. Si es válida -> Renueva la inactividad a 30 minutos desde ahora
    """
    if not raw_token:
        return None

    token_hash = hash_session_token(raw_token)
    sesion = session_db.query(Sesion).filter(Sesion.token_hash == token_hash).first()

    if not sesion or sesion.revoked:
        return None

    now = datetime.now(timezone.utc)
    expires_at = sesion.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if now >= expires_at:
        # Sesión vencida
        return None

    # Renovar vencimiento por inactividad a 30 minutos desde esta petición
    sesion.last_activity = now
    sesion.expires_at = now + timedelta(minutes=SESSION_INACTIVITY_MINUTES)
    session_db.commit()

    return sesion

def revoke_student_session(session_db: Session, raw_token: str | None) -> bool:
    """Revoca inmediatamente una sesión del lado del servidor."""
    if not raw_token:
        return False

    token_hash = hash_session_token(raw_token)
    sesion = session_db.query(Sesion).filter(Sesion.token_hash == token_hash).first()
    if sesion:
        sesion.revoked = True
        session_db.commit()
        return True
    return False

def cleanup_expired_sessions(session_db: Session) -> int:
    """Elimina sesiones vencidas de la base de datos de sesiones."""
    now = datetime.now(timezone.utc)
    deleted = session_db.query(Sesion).filter(
        (Sesion.revoked == True) | (Sesion.expires_at < now)
    ).delete(synchronize_session=False)
    session_db.commit()
    return deleted

