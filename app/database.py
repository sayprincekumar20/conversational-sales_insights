from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.config import settings

SQLALCHEMY_DATABASE_URL = f"sqlite:///{settings.NW_DB_PATH}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Create tables + extended view."""
    from app.models.northwind import Base
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        with open("app/db_init/create_views.sql") as f:
            conn.execute(text(f.read()))
