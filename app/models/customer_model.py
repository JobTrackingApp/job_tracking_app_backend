from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Customer(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None
    company_name: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)