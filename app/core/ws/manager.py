import asyncio
import logging
from typing import Optional
from fastapi.websockets import WebSocket
from starlette.websockets import WebSocketState
from app.core.auth import User
from app.core.auth.utils import authenticate_with_query
from app.core.exception import AuthFailedException
from app.crud.chat import save_chat, get_chat, remove_chat

logging = logging.getLogger(__name__)


class WsInstance:

    room_id: str
    websocket:WebSocket
    user: User

    def __init__(self, websocket, user) -> None:
        self.room_id = websocket.url.path
        self.websocket = websocket
        self.user = user


class WsConnectionManager:
    max_session: int

    def __init__(self, max_session = 3):
        self.connections = dict()
        self.max_session = max_session

    async def send_disconnect_message(self, websocket:WebSocket, message):
        message = {
            'status': 401,
            'message': message
        }
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_json(message)
        await websocket.close()

    async def connect(self, websocket:WebSocket, token: Optional[str]) -> WsInstance:
        try:
            await websocket.accept()
            user = await authenticate_with_query(token)
            instance = WsInstance(websocket=websocket, user=user)
            if not instance.room_id in self.connections:
                self.connections[instance.room_id] = []
            
            for state in self.connections[instance.room_id]:
                if state.user.username == user.username:
                    raise AuthFailedException(f'Tidak dapat membuka lebih dari {self.max_session} sesi')

            self.connections[instance.room_id].append(instance)
            logging.debug(f'{user.username} joined in {websocket.url.path}')
            logging.debug(f'{instance.room_id} has {len(self.connections[instance.room_id])} connections')
            return instance

        except AuthFailedException as e:
            args = e.args[0]
            await self.send_disconnect_message(websocket, args)

    async def broadcast(self, instance:WsInstance, data, ) -> bool:
        if not instance.room_id in self.connections:
            return False
        logging.debug(f'broadcasting {data} to {instance.room_id}')
        await asyncio.gather(*[instance.websocket.send_json(data) for state in self.connections[instance.room_id] if state != instance])
        return True

    async def p2p(self, instance: WsInstance, receiver: str, data):
        for state in self.connections[instance.room_id]:
            if state.user.username == receiver:
                message = {
                    'status': 200, # I dont know websocket proper status code lol
                    'data': data
                }
                await state.websocket.send_json(message)
                await remove_chat(receiver)
                return True
        await save_chat(data)
        return False


    async def disconnect(self, instance:WsInstance, message: str = 'Disconnected'):
        self.connections[instance.room_id].remove(instance)
        await self.send_disconnect_message(instance.websocket, message)
        logging.debug(f'user {instance.user.username} disconnected from {instance.room_id}')
        logging.debug(f'{instance.room_id} has {len(self.connections[instance.room_id])} connections')
