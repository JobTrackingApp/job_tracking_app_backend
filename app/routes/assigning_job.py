from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.models.assignment_model import AssignTechnician
from app.core.database import jobs_collection, users_collection

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs Assignment"]
)

@router.patch('/assign')
async def assign_technician(job_id :str, assignment: AssignTechnician):

    #Check whether the job exist
    job = await jobs_collection.find_one(
        {"job_id": job_id}
    )

    if not job_id:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )
    
    #Check technician exists
    technician = await jobs_collection.find_one(
        {
            "firebase_uid": assignment.technician_id,
            "role": "TECHNICIAN",
            "is_active": True
        }
    )

    if not technician:
        raise HTTPException(
            status_code=404,
            detail="Active technician not found"
        )

    #Update the job by assigning the technician
    result = await jobs_collection.update_one(
        {"job_id": job_id},
        {
            "$set": {
                "assigned_technician_id": assignment.technician_id,
                "updated_at": datetime.utcnow()
            }
        }
    )

    if result.matched_count == 0 :
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )
    
    updated_job = await jobs_collection.find_one(
        {"job_id": job_id}
    )

    return updated_job

@router.patch("/unassign")
async def unassign_technician(job_id: str):

    job = await jobs_collection.find_one(
        {"job_id": job_id}
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )
    
    if not job.get("assigned_technician_id"):
        raise HTTPException(
            status_code=404,
            detail="No technician is currently assigned"
        )
    
    await jobs_collection.find_one(
        {"job_id": job_id},
        {
            "$set" : {
                "assigned_technician_id": None,
                "updated_at": datetime.utcnow
            }
        }
    )

    updated_job = await jobs_collection.find_one(
        {"job_id": job_id}
    )

    return updated_job
    

