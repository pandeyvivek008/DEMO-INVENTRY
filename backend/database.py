"""
Database connection setup.

Default: SQLite file (inventory.db) - zero setup, perfect for a single-PC /
single-warehouse deployment. To move to PostgreSQL for multi-user / networked
access later, just set an environment variable before starting the server:

    export DATABASE_URL="postgresql://user:password@localhost:5432/inventory"

No code changes needed - SQLAlchemy handles both identically.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./inventory.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
# A bounded, pre-pinged PostgreSQL pool prevents each Uvicorn worker from
# opening unbounded connections under load. Tune these as a group with the
# managed database's connection limit, not per worker in isolation.
engine_options = {"connect_args": connect_args}
if not DATABASE_URL.startswith("sqlite"):
    engine_options.update({
        "pool_size": int(os.getenv("DB_POOL_SIZE", "10")),
        "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "10")),
        "pool_timeout": int(os.getenv("DB_POOL_TIMEOUT", "30")),
        "pool_pre_ping": True,
        "pool_recycle": int(os.getenv("DB_POOL_RECYCLE", "1800")),
    })
engine = create_engine(DATABASE_URL, **engine_options)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency - one DB session per request, always closed after."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
