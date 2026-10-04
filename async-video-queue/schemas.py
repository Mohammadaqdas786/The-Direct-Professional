from pydantic import BaseModel
from datetime import datetime

class JobCreate(BaseModel):
    filename: str
    resolution: str
    codec: str
    color_preset: str | None = "None"

class JobResponse(BaseModel):
    id: str
    filename: str
    status: str
    progress: int
    created_at: datetime

    class Config:
        from_attributes = True