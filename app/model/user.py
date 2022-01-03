from pydantic import BaseModel, Field
from typing import Optional

from app.core import config

from .utils import PyObjectId
from bson import ObjectId
from datetime import datetime

class User(BaseModel):
    id: str = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)
    customer_id: Optional[str]
    created: Optional[datetime] = datetime.now()
    updated: Optional[datetime] = datetime.now()
    photo: Optional[str] = f'/user/photo/profile.jpg'
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Done",
                "username": "janedone",
                "password": "mama",
            }
        }
