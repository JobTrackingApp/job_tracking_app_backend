from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum
from typing import Optional

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    RECEPTION = "RECEPTION"
    TECHNICIAN = "TECHNICIAN"

class User(BaseModel):
    name: str
    email: EmailStr
    phone: str
    role: UserRole
    is_active: bool = True
    firebase_uid: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()