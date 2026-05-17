import time
from app.db.database import SessionLocal
from app.db.models import Job
import pandas as pd
import os, json

while True:
  print("Checking for Jobs...")
  db = SessionLocal()
  job = None
  job = db.query(Job).filter(Job.status == "pending").first()
  if not job:
      print("No jobs")
      db.close()
      time.sleep(5)
      continue
  try:
    job.status = "running"
    db.commit()
    
    df = pd.read_csv(job.file_path)
    result = {
      "rows": df.shape[0],
      "columns": list(df.columns),
      "missing_values": df.isnull().sum().to_dict()
    }
    os.makedirs(f"data/results/{job.id}", exist_ok=True)
    
    result_path = f"data/results/{job.id}/result.json"
    with open(result_path, "w") as f:
      json.dump(result, f)
      
    job.result_path = result_path
    
    job.status = "done"
    db.commit()
    db.refresh(job)
    db.close()
    
  except Exception as e:
    if job:
      print(f"Error processing job {job.id}: {e}")
      job.status = "failed"
      db.commit()
      db.refresh(job)
      db.close()