import os

class Settings:
  Database_URL: str = os.getenv(
    "DATABASE_URL", "postgresql://user:password@localhost:5432/mydatabase"
    )

settings = Settings()