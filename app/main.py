from fastapi import FastAPI
from app.api.routes import router
from app.db.database import Base, engine
from app.db import models

Base.metadata.create_all(bind=engine)

app = FastAPI ()

app.include_router(router, prefix="/v1")