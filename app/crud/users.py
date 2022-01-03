from typing import List
from fastapi import HTTPException
from pydantic.tools import parse_obj_as
from app.api.v1.endpoints.user.serializers import UserData
from app.core.db import db
from .collection import USER_COLLECTION
from app.model.user import User

async def retrieve_user_by(username: str):
    user = await db[USER_COLLECTION].find_one({'username': username})
    if user:
        return user_helper(user)

async def create_user(user_data):
    find_user = await db[USER_COLLECTION].find_one({'username': user_data['username']})
    if find_user !=None:
        return
    user_in = await db[USER_COLLECTION].insert_one(user_data)
    new_user = await db[USER_COLLECTION].find_one({'_id': user_in.inserted_id})
    return user_helper(new_user)

async def retrieve_all_user():
    data_users = []
    async for users in db[USER_COLLECTION].find({}):
        data_users.append(user_helper(users))
    # return data_users
    return parse_obj_as(List[User], data_users)

async def check_username_exists(user: User):
    data = await db[USER_COLLECTION].find_one({'username': user.username})
    if data:
        raise HTTPException(
            status_code=409,
            detail=f'username: {user.username} exists'
        )
    return user

async def update_user(id_us: str, data: dict):
    if len(data) < 1:
        return False
    user = await db[USER_COLLECTION].find_one({'_id': id_us})
    if user is not None:
        id = data.get('id')
        if id != None:
            data.pop('id')
        update = await db[USER_COLLECTION].update_one(
            {'_id': id_us},
            {'$set': data}
        )
        user_updated = await db[USER_COLLECTION].find_one({'_id': id_us})
        if update is not None:
            return True, parse_obj_as(User, user_updated)
        return False, None
        
def user_helper(user) -> dict:
    return {
        'id': str(user.get('_id')),
        'name': user.get('name'),
        'username': user.get('username'),
        'password': user.get('password', None),
        'created': user.get('created', None),
        'updated': user.get('updated'),
        'photo': user.get('photo', 'profile.jpg'),
        'scopes': user.get('scopes', [])
    }   
