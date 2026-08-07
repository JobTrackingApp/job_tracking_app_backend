from datetime import datetime
from typing import Optional 
from pydantic import BaseModel, Field

class JobStatusHistory(BaseModel):
    job_id: int
    status: str = "RECEIVED"
    updated_by: str
    notes: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
