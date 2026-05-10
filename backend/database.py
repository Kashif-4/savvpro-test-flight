# database.py — SQLAlchemy engine, session factory, and dependency injector

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database stored in the backend directory
DATABASE_URL = "sqlite:///./flighthub.db"

# connect_args required for SQLite to allow use across threads (FastAPI runs multi-threaded)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Session factory — autoflush=False so we control when writes happen
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# Base class all ORM models inherit from
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that yields a DB session and guarantees cleanup.
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
