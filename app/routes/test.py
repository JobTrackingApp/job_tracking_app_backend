from fastapi import APIRouter
from app.core.database import db

router = APIRouter()

@router.get("/test-db")
async def test_db():

    collections = await db.list_collection_names()

    return {
        "status": "connected",
        "collections": collections
    }