from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime

class PaymentMethods(str, Enum):
    CASH = "CASH"
    ONLINE_TRANSACTION = "ONLINE_TRANSACTION"

class FinancialTransaction(BaseModel):
    job_id: int
    type: str = "CUSTOMER_PAYMENT"
    amount: int
    payment_method: PaymentMethods
    recorded_by: str
    date: datetime = Field(default_factory=datetime.utcnow)