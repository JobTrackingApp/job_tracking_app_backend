from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime

class PaymentMethod(str, Enum):
    CASH = "CASH"
    BANK_TRANSFER = "BANK_TRANSFER"
    CARD = "CARD"
    ONLINE_TRANSACTION = "ONLINE_TRANSACTION"


class CreatePayment(BaseModel):
    amount: int
    payment_method: PaymentMethod
    reference: str | None = None
    notes: str | None = None

class FinancialTransaction(BaseModel):
    job_id: str
    type: str = "CUSTOMER_PAYMENT"
    amount: int
    payment_method: PaymentMethod
    recorded_by: str
    reference: str | None = None
    notes: str | None = None
    date: datetime