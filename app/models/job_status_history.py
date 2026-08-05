from datetime import datetime 
from pydantic import BaseModel, Field

class JobStatusHistory(BaseModel):
    job_id: int
    status: str = "RECEIVED"
    updated_by: str
    notes: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
