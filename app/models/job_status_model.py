from enum import Enum
from pydantic import BaseModel


class JobStatus(str, Enum):
    RECEIVED = "RECEIVED"
    INSPECTION = "INSPECTION"
    WAITING_PARTS = "WAITING_PARTS"
    REPAIRING = "REPAIRING"
    COMPLETED = "COMPLETED"
    DELIVERED = "DELIVERED"
    UNREPAIRABLE = "UNREPAIRABLE"

class UpdateJobStatus(BaseModel):
    status: JobStatus
    notes: str | None = None