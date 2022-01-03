from typing import Optional
from pydantic import BaseModel
from time import time

class Media(BaseModel):
    type: str
    url: str
    thumbnail: str

class Chat(BaseModel):
    message: str
    sender: str
    receiver: str
    media: Optional[Media] = None
    timestamp: int = int(time() * 1000)

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'message': 'Hello World',
                'sender': 'admin',
                'receiver': 'user',
                'timestamp': '2020-01-01T00:00:00'
            }
        }