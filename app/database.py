# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection URL.
# This will be read from environment variables in a real application,
# but for Docker Compose, we'll use the service name 'db' for PostgreSQL.
DATABASE_URL = "postgresql://user:password@db/ecommerce"

# Create the SQLAlchemy engine.
# The 'echo=True' argument will log all SQL statements, which is useful for debugging.
engine = create_engine(DATABASE_URL, echo=True)

# Create a SessionLocal class.
# Each instance of SessionLocal will be a database session.
# The 'autocommit=False' means changes won't be committed automatically.
# The 'autoflush=False' means changes won't be flushed to the database automatically.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative models.
# All SQLAlchemy models will inherit from this Base.
Base = declarative_base()

# Dependency to get a database session.
# This function will be used with FastAPI's Depends to inject a database session
# into path operation functions.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()