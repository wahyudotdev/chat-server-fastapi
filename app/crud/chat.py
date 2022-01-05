from typing import List
from app.core.db import db
from .collection import CHAT_COLLECTION
from app.model.chat import Chat
from pydantic import parse_obj_as

async def save_chat(chat):
    chat_id = await db[CHAT_COLLECTION].insert_one(chat)
    return chat_id

async def get_chat(receiver: str):
    chats = await db[CHAT_COLLECTION].find({'receiver': receiver}).to_list(None)
    return parse_obj_as(List[Chat], chats)

async def remove_chat(receiver: str):
    await db[CHAT_COLLECTION].delete_many({'receiver': receiver})