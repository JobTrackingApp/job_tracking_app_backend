from fastapi import FastAPI
from app.routes.test import router as test_router
from app.routes.customers import router as customer_router
from app.routes.jobs import router as jobs_router
from app.routes.assigning_job import router as assignment_router
from app.routes.job_qr import router as qr_router
from app.routes.job_charges import router as charges_router
from app.routes.payments import router as payments_router
from app.routes.job_status import router as job_status_router

app = FastAPI(
    title="EasyFixFitSolutions Job Tracking API",
    version="1.0.0"
)

app.include_router(customer_router)
app.include_router(jobs_router)
app.include_router(assignment_router)
app.include_router(job_status_router)
app.include_router(qr_router)
app.include_router(charges_router)
app.include_router(payments_router)

@app.get("/")
async def root():
    return {
        "message": "EasyFixFitSolutions API is running"
    }