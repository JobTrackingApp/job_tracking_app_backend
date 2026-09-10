from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends

from app.core.database import jobs_collection, job_status_history_collection
from app.dependencies.auth import require_roles

router = APIRouter(
    prefix="/jobs",
    tags=["Job Status"]
)

#Updating job status
@router.get("/status-history")
async def get_status_history(
    job_id: str,
    current_user=Depends(
        require_roles("ADMIN", "RECEPTION", "TECHNICIAN")
    )):
    job = await jobs_collection.find_one(
        {"job_id": job_id}
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )
    
    history = await job_status_history_collection.find(
        {"job_id": job_id}
    ).sort(
        "timestamp", 1
    ).to_list(length=None)

    return history