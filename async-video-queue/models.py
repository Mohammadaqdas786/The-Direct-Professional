from sqlalchemy import Column, String, Integer, DateTime
from database import Base
import uuid
from datetime import datetime, timezone

class RenderJob(Base):
    __tablename__ = "render_jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    filename = Column(String, index=True)
    resolution = Column(String)
    codec = Column(String)
    color_preset = Column(String)
    
    status = Column(String, default="PENDING")
    progress = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))