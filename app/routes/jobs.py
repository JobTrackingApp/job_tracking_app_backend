from datetime import datetime
from fastapi import APIRouter, HTTPException

from app.models.job_model import CreateJob, UpdateJob, Job
from app.core.database import jobs_collection

router = APIRouter(
    prefix = "/jobs",
    tags= ["Jobs"]
)

#Create job
@router.post("/", response_model=Job)
async def create_job(job: CreateJob):
    last_job = await jobs_collection.find_one(
        sort=[("job_id", -1)])
    
    if last_job:
        last_number = int(last_job["job_id"].split("-")[1])
        job_id = f"JOB-{last_number + 1:06d}"
    else:
        job_id = "JOB-000001"

    time_now = datetime.utcnow()

    job_details = {
        "job_id": job_id,
        **job.model_dump(),
        "created_at": time_now,
        "updated_at": time_now
    }

    await jobs_collection.insert_one(job_details)

    return job_details

#Get all jobs
@router.get("/", response_model=list[Job])
async def get_jobs():
    jobs = await jobs_collection.find().to_list(length=None)

    return jobs

#Get job by job id
@router.get("/{job_id}", response_model=Job)
async def get_job(job_id: str):
    job = await jobs_collection.find_one(
        {"job_id": job_id}
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )
    
    return job

#Update job details
@router.patch("/job_id", response_model=Job)
async def update_job(job_id: str, job: UpdateJob):

    update_data = {
        key: value
        for key, value in job.model_dump().items()
        if value is not None
    }

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Failed to update job"
        )

    update_data["updated_at"] = datetime.utcnow()

    result = await jobs_collection.update_one(
        {"job_id": job_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    updated_job = await jobs_collection.find_one(
        {"job_id": job_id}
    )

    return updated_job