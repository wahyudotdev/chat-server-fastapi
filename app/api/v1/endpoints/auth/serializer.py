from pydantic import BaseModel

class TokenData(BaseModel):
    token: str
    expired: int

    class Config:
        orm_mode = True

class ResponseToken(BaseModel):
    status: int
    message: str
    access_token: str
    token_type: str
    data: TokenData

    class Config:
        orm_mode = True