from fastapi import FastAPI
import models
from database import engine

# Creates the database file on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Async Video Processing Queue")

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}