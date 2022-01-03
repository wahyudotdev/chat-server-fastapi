from fastapi import Depends, HTTPException, status
from fastapi.security import (OAuth2PasswordBearer, SecurityScopes)
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import timedelta, datetime

from app.core.config import API_V1_STR, SECRET_KEY
from app.crud.users import retrieve_user_by
from app.core.exception import AuthFailedException

from .jwt import ALGORITHM
from .serializers import User, TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth_scheme = OAuth2PasswordBearer(
    tokenUrl=API_V1_STR + "/auth/token"
)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(user, password: str):
    if not user:
        return False
    if not verify_password(password, user['password']):
        return False
    return user


async def get_current_user(security_scope: SecurityScopes, token: str = Depends(oauth_scheme)):
    if security_scope.scopes:
        authenticate_value = f'Bearer scope="{security_scope.scope_str}"'
    else:
        authenticate_value = f"Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(username=username, scopes=token_scopes)
    except JWTError:
        raise credentials_exception

    user = await retrieve_user_by(username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scope.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permission",
                headers={"WWW-Authenticate": authenticate_value}
            )
    return User(**user)

async def authenticate_with_query(token: str = None):
    if token == None:
        raise AuthFailedException('Membutuhkan query token, cth: chat/user_id?token=123asdahkhqke')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise AuthFailedException('Token tidak valid')
    username: str = payload.get("sub")
    if username is None:
        raise AuthFailedException('Autentikasi gagal')
    exp = datetime.fromtimestamp(payload.get('exp'))
    delta = timedelta(minutes=30)
    if datetime.now() - delta > exp:
        raise AuthFailedException('Token telah kadaluarsa')
    token_scopes = payload.get("scopes", [])
    token_data = TokenData(username=username, scopes=token_scopes)
    user = await retrieve_user_by(username=token_data.username)
    if user is None:
        raise AuthFailedException('Autentikasi gagal')
    return User(**user)
