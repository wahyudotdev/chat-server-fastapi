import json
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette.websockets import WebSocketDisconnect
from json.decoder import JSONDecodeError
from logging import getLogger
from app.core.ws import WsConnectionManager, WsInstance
from .serializer import Chat

logging = getLogger(__name__)
router = APIRouter()
room = WsConnectionManager()

@router.websocket('/')
async def private_chat(instance: WsInstance = Depends(room.connect)):
    if instance:
        while True:
            try:
                data = await instance.websocket.receive_json()
                data['sender'] = instance.user.username
                receiver = data['receiver']
                message = Chat(**data)
                await room.p2p(instance, receiver, jsonable_encoder(message))
            except JSONDecodeError:
                logging.error('JSONDecodeError')
                pass
            except WebSocketDisconnect:
                await room.disconnect(instance)
                break