from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()

class Job(Base):
  __tablename__ = "jobs"
  
  id = Column(String, primary_key=True)
  status = Column(String)