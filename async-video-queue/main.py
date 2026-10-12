import time
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal

# Creates the SQLite file and tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Async Video Processing Queue")

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- THE BACKGROUND WORKER ---
def process_video(job_id: str):
    db = SessionLocal()
    job = db.query(models.RenderJob).filter(models.RenderJob.id == job_id).first()
    
    if job:
        job.status = "PROCESSING"
        db.commit()
        
        # Simulate heavy video processing in 20% chunks
        for i in range(1, 6):
            time.sleep(2) 
            job.progress = i * 20
            db.commit()
            
        job.status = "COMPLETED"
        db.commit()
        
    db.close()

# --- THE API ENDPOINTS ---
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.post("/render", response_model=schemas.JobResponse, status_code=status.HTTP_202_ACCEPTED)
def create_render_job(job: schemas.JobCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    new_job = models.RenderJob(
        filename=job.filename,
        resolution=job.resolution,
        codec=job.codec,
        color_preset=job.color_preset
    )
    
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    
    background_tasks.add_task(process_video, new_job.id)
    return new_job

@app.get("/status/{job_id}", response_model=schemas.JobResponse)
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    job = db.query(models.RenderJob).filter(models.RenderJob.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    return job