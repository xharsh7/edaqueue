from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

engine = create_engine(settings.Database_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
    
Base = declarative_base()