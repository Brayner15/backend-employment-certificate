# app/routers/items.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["items"])
async def read_hello():
    return {"message": "Hello from items route"}
