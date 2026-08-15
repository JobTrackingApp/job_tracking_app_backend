from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in the environment variables")

if not DATABASE_NAME:
    raise ValueError("DATABASE_NAME is not set in the environment variables")

client = AsyncIOMotorClient(MONGO_URI)

db = client[DATABASE_NAME]

users_collection = db["users"]

customers_collection = db["customers"]

jobs_collection = db["jobs"]

job_status_history_collection = db["job_status_history"]

job_charges_collection = db["job_charges"]

financial_transactions_collection = db[
    "financial_transactions"
]