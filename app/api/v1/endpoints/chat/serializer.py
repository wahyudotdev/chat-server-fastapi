from typing import Optional
from pydantic import BaseModel

ALLOWED_CONTENT_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/*']

class Media(BaseModel):
    type: str
    url: str
    size: int

    class Config:
        orm_mode = True

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