import os
from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Base de datos independiente para sesiones
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SESSIONS_DB = f"sqlite:///{os.path.join(BASE_DIR, 'sessions.db').replace(os.sep, '/')}"

SESSIONS_DATABASE_URL = os.getenv("SESSIONS_DATABASE_URL", DEFAULT_SESSIONS_DB)

connect_args = {"check_same_thread": False} if "sqlite" in SESSIONS_DATABASE_URL else {}

session_engine = create_engine(
    SESSIONS_DATABASE_URL,
    connect_args=connect_args
)

SessionLocalSessions = sessionmaker(autocommit=False, autoflush=False, bind=session_engine)

SessionBase = declarative_base()

class Sesion(SessionBase):
    __tablename__ = "sesiones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token_hash = Column(String(64), unique=True, index=True, nullable=False)
    codigo_estudiante = Column(String(20), index=True, nullable=False)
    id_estudiante = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_activity = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)

class IntentoLogin(SessionBase):
    __tablename__ = "intentos_login"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip_address = Column(String(50), unique=True, index=True, nullable=False)
    failed_count = Column(Integer, default=0, nullable=False)
    last_failed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    blocked_until = Column(DateTime, nullable=True)

def init_session_db():
    SessionBase.metadata.create_all(bind=session_engine)

def get_session_db():
    db = SessionLocalSessions()
    try:
        yield db
    finally:
        db.close()

