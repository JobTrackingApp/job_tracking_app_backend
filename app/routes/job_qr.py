import secrets

from datetime import datetime
from fastapi import APIRouter, HTTPException

from app.core.database import jobs_collection
from app.models.qr_model import QRCodeResponse

router = APIRouter(
    prefix="/jobs",
    tags=["Job QR"]
)

@router.post("/qr", response_model=QRCodeResponse)
async def generate_qr(job_id: str):
    job = await jobs_collection.find_one(
        {"job_id": job_id}
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )
    
    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # If QR already exists, return existing token
    if job.get("qr_token"):
        return {
            "job_id": job_id,
            "qr_token": job["qr_token"]
        }

    # Generate secure random token
    qr_token = secrets.token_urlsafe(32)

    # Save token
    await jobs_collection.update_one(
        {"job_id": job_id},
        {
            "$set": {
                "qr_token": qr_token,
                "updated_at": datetime.utcnow()
            }
        }
    )

    return {
        "job_id": job_id,
        "qr_token": qr_token
    }

@router.get("/qr")
async def get_job_by_qr(qr_token: str):

    job = await jobs_collection.find_one(
        {"qr_token": qr_token}
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Invalid QR code"
        )

    return job