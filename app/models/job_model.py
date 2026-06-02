from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Job(BaseModel):
    job_number: int
    customer_name: str
    customer_phone: str
    item_type: str
    brand: str
    issue_description: str
    status: str = "RECEIVED"
    assigned_technician_id: Optional[str] = None
    qr_code: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    completed_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None