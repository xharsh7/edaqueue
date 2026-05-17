from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime
from app.db.database import Base 

class Job(Base):
  __tablename__ = "jobs"
  
  id = Column(String, primary_key=True)
  status = Column(String)
  
  file_path = Column(String)
  result_path = Column(String, nullable=True)
  
  created_at = Column(DateTime, default=datetime.utcnow)