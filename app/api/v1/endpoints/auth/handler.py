from time import time
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta

from app.core.auth import (authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES,
                            create_access_token, retrieve_user_by)

from .serializer import ResponseToken, TokenData

router = APIRouter()


@router.post('/token', response_model=ResponseToken)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    data_user = await retrieve_user_by(form_data.username)
    user = authenticate_user(data_user, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorect Username or pasword",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    scope_user = user['scopes']
    access_token = create_access_token(
        data={"sub": user['username'], "scopes": scope_user},
        expires_delta=access_token_expires
    )
    data = TokenData(
        token = access_token,
        expired = time() + ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    ResponseToken.status = status.HTTP_200_OK
    ResponseToken.message = "Success"
    ResponseToken.access_token = access_token
    ResponseToken.token_type = "bearer"
    ResponseToken.data = data
    return ResponseToken