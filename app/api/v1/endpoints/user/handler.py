import logging
from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse

from .serializers import ResponseUserInDB, ResponseUsers, UpdateUser
from .utils import encrypt_password
from app.core.auth import User, get_current_user
from app.crud.users import (check_username_exists, retrieve_all_user,
                            create_user, retrieve_user_by, update_user)


router = APIRouter()

@router.post(path='/create', response_model=ResponseUserInDB)
async def add_user(user_data: User = Depends(check_username_exists)):
    user_data = jsonable_encoder(user_data)
    user_data['password'] = encrypt_password(user_data['password'])

    data_new = await create_user(user_data)

    ResponseUserInDB.message = "Create New Account Success..."
    ResponseUserInDB.data = data_new

    return ResponseUserInDB

@router.get('/all', response_model=ResponseUsers)
async def get_all_user(current_user: User = Depends(get_current_user)):
    try:
        users = await retrieve_all_user()
        users = [user for user in users if user.username != current_user.username]
        ResponseUsers.data = users
    except Exception as e:
        print("Error : ", e)
    return ResponseUsers


@router.get('/profile', response_model=ResponseUserInDB)
async def get_self_profile(current_user: User = Depends(get_current_user)):
    try:
        user_data = await retrieve_user_by(username=current_user.username)
        if user_data is not None:
            ResponseUserInDB.message = "User Data"
            ResponseUserInDB.data = user_data
    except Exception as e:
        logging.error("Error get dettail user : ", e)
        ResponseUserInDB.message = "Tidak ada Data yang sesuai dengan ID yang dicari"

    return ResponseUserInDB


@router.post('/profile',  response_model=ResponseUserInDB)
async def update_self_profile(data_update: UpdateUser, user=Depends(get_current_user)):
    data_user = {k: v for k, v in data_update.dict().items() if v is not None}
    success, updated_user = await update_user(user.id, data_user)
    ResponseUserInDB.message = "Berhasil memperbarui profil" if success else "Pembaruan profil gagal"
    ResponseUserInDB.data = updated_user
    ResponseUserInDB.status = success
    return ResponseUserInDB


@router.get('/photo/{picture}', dependencies=[Depends(get_current_user)])
async def get_user_photo(picture: str):
    try:
        return FileResponse(
            path=f'app/static/images/{picture}',
            media_type='image/jpeg'
        )
    except Exception as e:
        return HTTPException(
            status_code=404,
            detail='Foto tidak ditemukan'
        )

