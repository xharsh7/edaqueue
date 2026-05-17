import json
from fastapi import BackgroundTasks
from fastapi import APIRouter, Depends, UploadFile
import os
import uuid
from app.db.database import SessionLocal
from sqlalchemy.orm import Session
from app.db.models import Job
from app.db.database import get_db
router = APIRouter()

UPLOAD_DIR = "data"

@router.get("/health")
def health_check():
  return {"status": "ok"}

@router.post("/upload")
def upload_file(
  file: UploadFile, 
  background_tasks: BackgroundTasks,
  db: Session = Depends(get_db)
  ):
  file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
  
  with open(file_path, "wb") as f:
    f.write(file.file.read())
    
  job = Job(
    id = str(uuid.uuid4()),
    status = "pending",
    file_path = file_path
  )
  
  db.add(job)
  db.commit()
  db.refresh(job)
  
  background_tasks.add_task(process_job, job.id)
  return {
    "job_id": job.id,
    "status": job.status
    }
  
@router.get("/job/{job_id}")
def get_job_status(job_id: str, db: Session = Depends(get_db)):
  job = db.query(Job).filter(Job.id == job_id).first()
  if not job:
    return {"error": "Job not found"}
  
  if job.status != "done":
    return {
      "id": job.id, 
      "status": job.status
      }
    
  if not job.result_path:
    return {
        "id": job.id,
        "status": job.status,
        "error": "Result not available"
    }
  
  with open(job.result_path, "r") as f:
    result = json.load(f)
  return{
    "id" : job.id,
    "status" : job.status,
    "result" : result
  }
  
@router.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
  jobs = db.query(Job).all()
  return [
    {
      "id": job.id,
      "status": job.status,
      "created_at": job.created_at
    }
    for job in jobs
  ]