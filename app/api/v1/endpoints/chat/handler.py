from time import time
from fastapi import APIRouter, Depends, HTTPException
from fastapi.datastructures import UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.params import File
from starlette.requests import Request
from starlette.responses import FileResponse
from starlette.websockets import WebSocketDisconnect
from json.decoder import JSONDecodeError
from logging import getLogger
from app.core.config.config import API_V1_STR
from app.core.ws import WsConnectionManager, WsInstance
from app.crud.chat import remove_chat
from .serializer import ALLOWED_CONTENT_TYPES, Chat, Media
from app.crud import get_chat
from app.core.auth import get_current_user
from uuid import uuid4

logging = getLogger(__name__)
router = APIRouter()
room = WsConnectionManager()

@router.websocket('/')
async def private_chat(instance: WsInstance = Depends(room.connect)):
    if instance:
        while True:
            try:
                data = await instance.websocket.receive_json()
                if data.get('event') == 'message':
                    data['sender'] = instance.user.username
                    data['timestamp'] = int(time() * 1000)
                    data['name'] = instance.user.name
                    receiver = data['receiver']
                    message = Chat(**data)
                    await room.p2p(instance, receiver, jsonable_encoder(message))
                elif data.get('event') == 'refresh':
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

@router.post('/file', response_model=Media)
async def send_file(request: Request, user = Depends(get_current_user), file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(400, detail=f"{file.content_type} is invalid document type")
    save_file = await file.read()
    ext = file.filename.split('.')[-1]
    file_name = str(uuid4()) + '.' + ext
    with open(f"app/static/user_files/{file_name}", "wb") as f:
            f.write(save_file)
    Media.url = request.url.scheme+'://'+request.url.netloc+API_V1_STR+'/chat/file/'+file_name
    Media.type = file.content_type
    Media.size = save_file.__sizeof__()
    return Media

@router.get('/file/{filename}')
async def get_file(filename: str):
    return FileResponse(
        path=f'app/static/user_files/{filename}'
    )
