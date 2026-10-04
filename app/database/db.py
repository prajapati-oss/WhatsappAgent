import os
import logging

from contextlib import contextmanager

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError


# =========================================================
# LOAD ENV VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# LOGGING CONFIG
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# =========================================================
# DATABASE URL
# =========================================================

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL not found in .env file")


# =========================================================
# SQLALCHEMY ENGINE
# =========================================================

engine = create_engine(
    DATABASE_URL,

    # Connection Pool Settings
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,

    # Validates stale DB connections
    pool_pre_ping=True,

    # SQL query logs
    echo=False
)


# =========================================================
# SESSION FACTORY
# =========================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# =========================================================
# BASE MODEL CLASS
# =========================================================

Base = declarative_base()


# =========================================================
# FASTAPI DATABASE DEPENDENCY
# =========================================================

def get_db():
    """
    FastAPI dependency injection for DB sessions.
    """

    db = SessionLocal()

    try:
        yield db

    except SQLAlchemyError as e:

        logger.error(f"Database Error: {str(e)}")

        db.rollback()

        raise

    finally:
        db.close()


# =========================================================
# MANUAL DATABASE SESSION
# =========================================================

@contextmanager
def db_session():
    """
    Manual database session manager.
    Useful for services/scripts/background tasks.
    """

    db = SessionLocal()

    try:

        yield db

        db.commit()

    except Exception as e:

        db.rollback()

        logger.error(f"Transaction Failed: {str(e)}")

        raise

    finally:

        db.close()


# =========================================================
# DATABASE HEALTH CHECK
# =========================================================

def check_database_connection():
    """
    Test PostgreSQL connection.
    """

    try:

        db = SessionLocal()

        logger.info("✅ PostgreSQL connected successfully")

        db.close()

    except Exception as e:

        logger.error(f"❌ Database connection failed: {str(e)}")


# =========================================================
# CREATE TABLES
# =========================================================

def init_db():
    """
    Create all database tables.
    """

    from app.database.models import User, Conversation

    Base.metadata.create_all(bind=engine)

    logger.info("✅ Database tables initialized")