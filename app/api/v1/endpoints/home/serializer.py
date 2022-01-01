from pydantic import BaseModel

class Greeting(BaseModel):
    message: str