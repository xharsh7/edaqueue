import os

class Settings:
  Database_URL: str = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/job_db"
    )

settings = Settings()