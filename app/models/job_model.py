from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Job(BaseModel):
    job_id: int
    customer_id: str
    item_type: str
    brand: str
    issue_description: str
    status: str = "RECEIVED"
    assigned_technician_id: Optional[str] = None
    qr_code: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None