from typing import Optional
from uuid import uuid4
import asyncio
import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import WebSocketException, HTTPException
from pydantic import UUID4

from app.utils.clients import rooms, clients
from app.utils.actions import Actions


router = APIRouter()


@router.post("/create_room/{room_id}")
async def create_room(room_id: str, user_id: str, is_group: bool = False):
    room = rooms.create_room(room_id=room_id, owner_id=user_id, is_group=is_group)
    return JSONResponse({"room_id": str(room.id), "is_group": room.is_group})


@router.post("/join_room")
async def join_room(room_id: str, client_id: str, client_name: Optional[str] = None):

    client = clients.get_client(client_id=client_id)
    if client is None:
        client = clients.create_client(client_id=client_id, name=client_name)
    room = client.get_room()

    if room is not None:
        await room.remove_client(client_id=client.id)

    room = rooms.get_room(room_id=room_id)
    if room is None:
        return HTTPException(
            status_code=404,
            detail="The room with this id does not exist"
        )
    
    room.add_client(client=client)
    client.set_room(room=room)
    return JSONResponse({"room_id": str(room.id), "client_id": str(client.id), "is_group": room.is_group})


@router.websocket("/lobby")
async def websocket_lobby_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            await websocket.send_json({"type": Actions.SHARE_ROOMS.value, "rooms": rooms.get_rooms_info()})
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        return
            

# TODO make messages receiving
@router.websocket("/ws/{client_id}")
async def websocket_room_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    
    client = clients.get_client(client_id=client_id)
    if client is None:
        raise WebSocketException(
            code=1007,
            reason="The client with this uuid does not exist"
        )
    room = client.get_room()

    if room is None:
        raise WebSocketException(
            code=1007,
            reason="The room with this uuid does not exist"
        )
    
    client.open(websocket=websocket)

    try:
        while True:
            try:
                data = await websocket.receive()
                if data is not None:
                    await client.handle_message(message=data, room=room)
            except RuntimeError:
                break
    except WebSocketDisconnect:
        await client.handle_disconnect(room=room)
        await clients.delete_client(client_id=client_id)
