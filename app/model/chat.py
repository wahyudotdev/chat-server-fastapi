from pydantic import BaseModel
from typing import Optional

class Media(BaseModel):
    type: str
    url: str
    thumbnail: str

class Chat(BaseModel):
    name: str
    message: str
    sender: str
    receiver: str
    media: Optional[Media] = None
    timestamp: int

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