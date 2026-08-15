from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.core.database import (
    jobs_collection,
    job_charges_collection
)

from app.models.charges_model import (
    CreateJobCharges,
    UpdateJobCharges
)


router = APIRouter(
    prefix="/jobs",
    tags=["Job Charges"]
)


@router.post("/charges")
async def create_job_charges(
    job_id: str,
    charges: CreateJobCharges
):

    # Check job exists
    job = await jobs_collection.find_one(
        {"job_id": job_id}
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # Prevent duplicate charge records
    existing = await job_charges_collection.find_one(
        {"job_id": job_id}
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Charges already exist for this job"
        )

    customer_total = (
        charges.repair_charge
        + charges.parts_charge
        + charges.other_charge
    )

    total_cost = (
        charges.parts_cost
        + charges.technician_cost
        + charges.other_cost
    )

    gross_profit = customer_total - total_cost

    charge_data = {
        "job_id": job_id,

        "repair_charge": charges.repair_charge,
        "parts_charge": charges.parts_charge,
        "other_charge": charges.other_charge,

        "customer_total": customer_total,

        "parts_cost": charges.parts_cost,
        "technician_cost": charges.technician_cost,
        "other_cost": charges.other_cost,

        "total_cost": total_cost,
        "gross_profit": gross_profit,

        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    await job_charges_collection.insert_one(
        charge_data
    )

    return charge_data

@router.get("/charges")
async def get_job_charges(job_id: str):

    charges = await job_charges_collection.find_one(
        {"job_id": job_id}
    )

    if not charges:
        raise HTTPException(
            status_code=404,
            detail="Charges not found for this job"
        )

    return charges

@router.patch("/charges")
async def update_job_charges(
    job_id: str,
    charges: UpdateJobCharges
):

    existing = await job_charges_collection.find_one(
        {"job_id": job_id}
    )

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Charges not found for this job"
        )

    update_data = {
        key: value
        for key, value in charges.model_dump().items()
        if value is not None
    }

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No charge information provided"
        )

    # Merge old + new values
    repair_charge = update_data.get(
        "repair_charge",
        existing.get("repair_charge", 0)
    )

    parts_charge = update_data.get(
        "parts_charge",
        existing.get("parts_charge", 0)
    )

    other_charge = update_data.get(
        "other_charge",
        existing.get("other_charge", 0)
    )

    parts_cost = update_data.get(
        "parts_cost",
        existing.get("parts_cost", 0)
    )

    technician_cost = update_data.get(
        "technician_cost",
        existing.get("technician_cost", 0)
    )

    other_cost = update_data.get(
        "other_cost",
        existing.get("other_cost", 0)
    )

    customer_total = (
        repair_charge
        + parts_charge
        + other_charge
    )

    total_cost = (
        parts_cost
        + technician_cost
        + other_cost
    )

    gross_profit = customer_total - total_cost

    update_data.update({
        "customer_total": customer_total,
        "total_cost": total_cost,
        "gross_profit": gross_profit,
        "updated_at": datetime.utcnow()
    })

    await job_charges_collection.update_one(
        {"job_id": job_id},
        {"$set": update_data}
    )

    updated = await job_charges_collection.find_one(
        {"job_id": job_id}
    )

    return updated