from fastapi import FastAPI
# from app.routes.test import router as test_router
from app.routes.customers import router as customer_route

app = FastAPI(
    title="EasyFixFitSolutions Job Tracking API",
    version="1.0.0"
)

app.include_router(customer_route)