from fastapi import APIRouter

from app.api.v1.endpoints.home.serializer import Greeting

router = APIRouter()

@router.get("/", response_model=Greeting)
async def read_root():
    return Greeting(message="Hello World!")