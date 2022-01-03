from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class UserInDb(BaseModel):
    name: Optional[str]
    username: Optional[str]
    password: Optional[str]


class UserData(BaseModel):
    id: str
    name: str
    username: str
    created: Optional[datetime]
    updated: Optional[datetime]
    photo: Optional[str] = None
    
    class Config:
        orm_mode = True
        schema_extra = {
                'example': {
                    "id": "61c8903d41a207fe6a9c24cf",
                    "name": "Customer Account",
                    "username": "customer",
                    "created": "2021-12-26T22:52:52.603004",
                    "updated": "2021-12-26T22:52:52.603007",
                    "photo": "/isl/api/v1/user/photo/profile.jpg"
                }
        }


class UpdateUser(BaseModel):
    name: Optional[str]
    email: Optional[str]
    updated: Optional[datetime] = datetime.now()
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Jane Done",
                "email": "janedoe@gmail.com"
            }
        }


class ResponseUserInDB(BaseModel):
    status: int = 200
    message: Optional[str]
    data: Optional[UserData]

    class Config:
        orm_mode = True


class ResponseUsers(BaseModel):
    status: int = 200
    message: Optional[str] = "Success Get All Users"
    data: List[UserData] = []

    class Config:
        orm_mode = True