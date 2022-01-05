from time import time
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette.websockets import WebSocketDisconnect
from json.decoder import JSONDecodeError
from logging import getLogger
from app.core.ws import WsConnectionManager, WsInstance
from app.crud.chat import remove_chat
from .serializer import Chat
from app.crud import get_chat
from app.core.auth import get_current_user

logging = getLogger(__name__)
router = APIRouter()
room = WsConnectionManager()

@router.websocket('/')
async def private_chat(instance: WsInstance = Depends(room.connect)):
    if instance:
        while True:
            try:
                data = await instance.websocket.receive_json()
                if data['event'] == 'message':
                    data['sender'] = instance.user.username
                    data['timestamp'] = int(time() * 1000)
                    data['name'] = instance.user.name
                    receiver = data['receiver']
                    message = Chat(**data)
                    await room.p2p(instance, receiver, jsonable_encoder(message))
                elif data['event'] == 'refresh':
                    pending_chat = await get_chat(instance.user.username)
                    for message in pending_chat:
                        await instance.websocket.send_json(jsonable_encoder(message))
                    await remove_chat(instance.user.username)
            except JSONDecodeError:
                logging.error('JSONDecodeError')
                pass
            except WebSocketDisconnect:
                await room.disconnect(instance)
                break

@router.get('/', response_model=list)
async def get_chats(user = Depends(get_current_user)):
    pending_chat = await get_chat(user.username)
    await remove_chat(user.username)
    return pending_chat