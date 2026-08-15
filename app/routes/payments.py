from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.core.database import (
    jobs_collection,
    job_charges_collection,
    financial_transactions_collection
)

from app.models.financial_transactions import CreatePayment


router = APIRouter(
    prefix="/jobs",
    tags=["Job Payments"]
)


@router.post("/payment")
async def record_payment(
    job_id: str,
    payment: CreatePayment
):

    # Check job
    job = await jobs_collection.find_one(
        {"job_id": job_id}
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # Get charges
    charges = await job_charges_collection.find_one(
        {"job_id": job_id}
    )

    if not charges:
        raise HTTPException(
            status_code=404,
            detail="Charges have not been created for this job"
        )

    customer_total = charges.get(
        "customer_total",
        0
    )

    # Get previous payments
    previous_payments = await financial_transactions_collection.find(
        {
            "job_id": job_id,
            "type": "CUSTOMER_PAYMENT"
        }
    ).to_list(length=None)

    amount_paid = sum(
        payment_record.get("amount", 0)
        for payment_record in previous_payments
    )

    outstanding = customer_total - amount_paid

    # Prevent overpayment
    if payment.amount > outstanding:
        raise HTTPException(
            status_code=400,
            detail=f"Payment exceeds outstanding balance of Rs. {outstanding}"
        )

    transaction = {
        "job_id": job_id,
        "type": "CUSTOMER_PAYMENT",
        "amount": payment.amount,
        "payment_method": payment.payment_method.value,
        "reference": payment.reference,
        "notes": payment.notes,
        "recorded_by": "TEMP_USER",
        "date": datetime.utcnow()
    }

    result = await financial_transactions_collection.insert_one(
        transaction
    )

    # Calculate new balance
    new_amount_paid = amount_paid + payment.amount
    new_outstanding = customer_total - new_amount_paid

    return {
        "transaction_id": str(result.inserted_id),
        "job_id": job_id,
        "payment_amount": payment.amount,
        "amount_paid": new_amount_paid,
        "customer_total": customer_total,
        "outstanding": new_outstanding,
        "payment_method": payment.payment_method
    }

@router.get("/payments")
async def get_job_payments(job_id: str):

    payments = await financial_transactions_collection.find(
        {
            "job_id": job_id,
            "type": "CUSTOMER_PAYMENT"
        }
    ).sort(
        "date", 1
    ).to_list(length=None)

    return payments