from datetime import datetime
from typing import List, Optional
from uuid import uuid4, UUID
import json

from fastapi import WebSocket
from pydantic import UUID4
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCIceCandidate, RTCIceServer, RTCConfiguration

from app.utils.actions import Actions, DeviceTypes
from app.utils.chat import Message, Chat
from app.utils.recording import Recorder


class Client:
    def __init__(self, client_id: str, name: Optional[str] = None, room: Optional["Room"] = None) -> None:
        self.id = client_id
        self.name: str = name or f"Undefined{self.id}"
        self.websocket: Optional[WebSocket] = None
        self.room: Optional[Room] = room
        self.camera_toggle: Optional[bool] = False
        self.microphone_toggle: Optional[bool] = False
        self.screen_sharing_toggle: Optional[bool] = False
        self.device_type: Optional[DeviceTypes] = DeviceTypes.DESKTOP.value
        self.pc: Optional[RTCPeerConnection] = None
        self.recorder: Optional[Recorder] = None

    async def setup_rtc(self):
        """Set up RTC connection and attach a recorder."""
        ice_server = RTCIceServer(urls=['stun:stun.l.google.com:19302'])
        config = RTCConfiguration(iceServers=[ice_server])

        self.pc = RTCPeerConnection(configuration=config)

        if self.recorder is None:
            self.recorder = Recorder(self.room.id, self.id)
            self.recorder.setup()

        @self.pc.on("track")
        async def on_track(track):
            print("Got track:", track, track)

            self.recorder.add_track(track)

            await self.recorder.start()
            print("Recording started for the first track.")

        @self.pc.on("iceconnectionstatechange")
        async def on_ice_connection_state_change():
            print(f"ICE connection state changed: {self.pc.iceConnectionState}")
            if self.pc.iceConnectionState == "failed":
                print("ICE connection failed. Closing connection.")
                await self.close()
            else:
                print("ICE connection state changed:", self.pc.iceConnectionState)

        @self.pc.on("icecandidate")
        async def on_ice_candidate(event):
            print("ICE CANDIDATE", event)

        @self.pc.on("datachannel")
        async def on_datachannel(channel):
            print(f"changed datachannel to {channel}")

        @self.pc.on("signalingstatechange")
        async def on_signalingstatechange():
            print(f"changed signalingstatechange {self.pc.signalingState}")

        @self.pc.on("icegatheringstatechange")
        async def on_icegatheringstatechange():
            print(f"changed icegatheringstatechange {self.pc.iceGatheringState}")

    # async def start_recording(self):
    #     """Start the recorder."""
    #     if self.recorder:
    #         await self.recorder.start()

    # async def stop_recording(self):
    #     """Stop the recorder."""
    #     if self.recorder:
    #         await self.recorder.stop()

    def get_room(self) -> Optional["Room"]:
        return self.room
    
    def set_room(self, room: "Room"):
        self.room = room

    def open(self, websocket: Optional[WebSocket] = None) -> None:
        self.websocket = websocket

    def to_dict(self) -> dict:
        return {
            "id": str(self.id)
        }
    
    def get_toggles(self) -> dict:
        return {
            "camera_toggle": self.camera_toggle,
            "microphone_toggle": self.microphone_toggle,
            "screen_sharing_toggle": self.screen_sharing_toggle
        }

    async def handle_join(self, data, room: "Room"):
        client_id = data["client_id"]
        is_viewer = data.get("is_viewer", False)
        toggles = data.get("toggles", {})
        camera_toggle = toggles.get("camera_toggle", False)
        microphone_toggle = toggles.get("microphone_toggle", False)
        screen_sharing_toggle = toggles.get("screen_sharing_toggle", False)
        device_type = data.get("device_type", DeviceTypes.DESKTOP.value)
        orientation = data.get("orientation", "landscape")

        self.camera_toggle = camera_toggle
        self.microphone_toggle = microphone_toggle
        self.screen_sharing_toggle = screen_sharing_toggle
        self.device_type = device_type
        self.orientation = orientation

        clients = room.get_clients()
        toggles = self.get_toggles()

        if is_viewer:
            for client in clients:
                if client.websocket is not None:
                    await client.websocket.send_json({"type": Actions.ADD_PEER.value, "payload": { "peerID": client_id, 
                                                                                                   "client_name": self.name, 
                                                                                                   "createOffer": False, 
                                                                                                   "is_viewer": is_viewer, 
                                                                                                   "toggles": toggles, 
                                                                                                   "device_type": self.device_type,
                                                                                                   "orientation": self.orientation}})
                if self.websocket is not None:
                    await self.websocket.send_json({"type": Actions.ADD_PEER.value, "payload": { "peerID": str(client.id), 
                                                                                                 "client_name": client.name, 
                                                                                                 "createOffer": True, 
                                                                                                 "is_viewer": is_viewer, 
                                                                                                 "toggles": client.get_toggles(), 
                                                                                                 "device_type": client.device_type,
                                                                                                 "orientation": client.orientation}})  
            
        else:    
            for client in clients:
                if client.websocket is not None:
                    await client.websocket.send_json({"type": Actions.ADD_PEER.value, "payload": { "peerID": client_id, 
                                                                                                   "client_name": self.name, 
                                                                                                   "createOffer": True, 
                                                                                                   "is_viewer": is_viewer, 
                                                                                                   "toggles": toggles, 
                                                                                                   "device_type": self.device_type,
                                                                                                   "orientation": self.orientation}})
                if self.websocket is not None:
                    await self.websocket.send_json({"type": Actions.ADD_PEER.value, "payload": { "peerID": str(client.id), 
                                                                                                 "client_name": client.name, 
                                                                                                 "createOffer": False, 
                                                                                                 "is_viewer": is_viewer, 
                                                                                                 "toggles": client.get_toggles(), 
                                                                                                 "device_type": client.device_type,
                                                                                                 "orientation": client.orientation}})  

        data = await room.get_all_messages()
        await self.websocket.send_json(data)

        owner_id = room.get_owner()
        await self.websocket.send_json(
            {
                "type": Actions.OWNER.value,
                "payload": owner_id
            }
        )

        client_name = self.name
        await self.websocket.send_json(
            {
                "type": Actions.YOUR_NAME.value,
                "payload": client_name
            }
        )

        room.add_client(self)

        await self.setup_rtc() 
        # await self.start_recording() 

    async def handle_leave(self, data, room: "Room"):
        client_id = data["client_id"]

        clients = room.get_clients()

        await room.remove_client(self.id)

        for client in clients:
            if client.websocket is not None:
                await client.websocket.send_json({"type": Actions.REMOVE_PEER.value, "payload": { "peerID": client_id }})
            if self.websocket is not None:
                await self.websocket.send_json({"type": Actions.REMOVE_PEER.value, "payload": { "peerID": str(client.id) }})

        await self.websocket.close()
        self.websocket = None

        await self.stop_recording()  # Stop recording
        if self.pc:
            await self.pc.close()  # Close RTC connection
            self.pc = None

    async def handle_disconnect(self, room: "Room"):
        clients = room.get_clients()

        await room.remove_client(self.id)

        for client in clients:
            if client.websocket is not None:
                await client.websocket.send_json({"type": Actions.REMOVE_PEER.value, "payload": { "peerID": str(self.id) }})

        if self.recorder:
            await self.recorder.stop()  # Stop the recording

        # Close WebSocket connection
        if self.websocket is not None:
            await self.websocket.close()
        self.websocket = None

        # Close RTC connection if exists
        if self.pc:
            await self.pc.close()
            self.pc = None

    async def handle_relay_sdp(self, data, room: "Room"): 
        peer_id = data["peerID"]
        session_description = data["sessionDescription"]
        type = data["type"]

        client = room.get_client(client_id=peer_id)

        await client.websocket.send_json({"type": Actions.SESSION_DESCRIPTION.value, "payload": { "peerID": str(self.id), "sessionDescription": session_description, "type": type}})

    async def handle_relay_ice(self, data, room: "Room"):
        peer_id = data["peerID"]
        ice_candidate = data["iceCandidate"]

        client = room.get_client(client_id=peer_id)

        if client.websocket is not None:
            await client.websocket.send_json({"type": Actions.ICE_CANDIDATE.value, "payload": { "peerID": str(self.id), "iceCandidate": ice_candidate}})

    async def handle_new_message(self, data, room: "Room") -> None:
        clients = room.get_clients()
        data = await room.send_chat_message(client_id=self.id, message=data)

        for client in clients:
            if client.websocket is not None:
                await client.websocket.send_json(data)

    async def handle_started_screen_sharing(self, data, room: "Room"):
        clients = room.get_clients()

        for client in clients:
            if client.id != self.id and client.websocket is not None:
                await client.websocket.send_json({"type": Actions.STARTED_SCREEN_SHARING.value, "payload": { "peerID": str(self.id) }})

        self.screen_sharing_toggle = True

    async def handle_stopped_screen_sharing(self, data, room: "Room"):
        clients = room.get_clients()

        for client in clients:
            if client.id != self.id and client.websocket is not None:
                await client.websocket.send_json({"type": Actions.STOPPED_SCREEN_SHARING.value, "payload": { "peerID": str(self.id) }})

        self.screen_sharing_toggle = False

    async def handle_enable_camera(self, data, room: "Room"):
        clients = room.get_clients()

        for client in clients:
            if client.id != self.id and client.websocket is not None:
                await client.websocket.send_json({"type": Actions.ENABLE_CAMERA.value, "payload": { "peerID": str(self.id) }})

        self.camera_toggle = True

    async def handle_disable_camera(self, data, room: "Room"):
        clients = room.get_clients()

        for client in clients:
            if client.id != self.id and client.websocket is not None:
                await client.websocket.send_json({"type": Actions.DISABLE_CAMERA.value, "payload": { "peerID": str(self.id) }})

        self.camera_toggle = False

    async def handle_enable_microphone(self, data, room: "Room"):
        clients = room.get_clients()

        for client in clients:
            if client.id != self.id and client.websocket is not None:
                await client.websocket.send_json({"type": Actions.ENABLE_MICROPHONE.value, "payload": { "peerID": str(self.id) }})

        self.microphone_toggle = True

    async def handle_disable_microphone(self, data, room: "Room"):
        clients = room.get_clients()

        for client in clients:
            if client.id != self.id and client.websocket is not None:
                await client.websocket.send_json({"type": Actions.DISABLE_MICROPHONE.value, "payload": { "peerID": str(self.id) }})

        self.microphone_toggle = False

    async def handle_rotate(self, data, room: "Room"):
        clients = room.get_clients()

        for client in clients:
            if client.id != self.id and client.websocket is not None:
                await client.websocket.send_json({"type": Actions.ROTATE.value, "payload": { "peerID": str(self.id), "orientation": self.orientation }})

        self.orientation = data["orientation"]

    async def handle_end_call(self, data, room: "Room"):
        clients = room.get_clients()

        for client in clients:
            await client.websocket.send_json({"type": Actions.END_CALL.value})

    async def handle_ping(self): 
        if self.websocket is not None:
            await self.websocket.send_json({"type": Actions.PONG.value})

    async def handle_offer(self, data, room: "Room"):
        offer = RTCSessionDescription(sdp=data["sdp"], type=data["type"])
        # offer = RTCSessionDescription(data)

        await self.pc.setRemoteDescription(offer)
        answer = await self.pc.createAnswer()
        await self.pc.setLocalDescription(answer)

        if self.websocket is not None:
            await self.websocket.send_json({"type": Actions.SERVER_ANSWER.value, 
                                            "payload": { "sdp": self.pc.localDescription.sdp, 
                                                         "type": self.pc.localDescription.type }})

    async def handle_server_ice(self, data, room: "Room"):
        candidate = data["iceCandidate"]
        if candidate["candidate"] == "":
            return 
        ip = candidate["candidate"].split(" ")[4]
        port = candidate["candidate"].split(" ")[5]
        protocol = candidate["candidate"].split(" ")[7]
        priority = candidate["candidate"].split(" ")[3]
        foundation = candidate["candidate"].split(" ")[0]
        component = candidate["candidate"].split(" ")[1]
        type = candidate["candidate"].split(" ")[7]
        ice_candidate = RTCIceCandidate(
            ip=ip,
            port=port,
            protocol=protocol,
            priority=priority,
            foundation=foundation,
            component=component,
            type=type,
            sdpMid=candidate["sdpMid"],
            sdpMLineIndex=candidate["sdpMLineIndex"]
        )

        await self.pc.addIceCandidate(ice_candidate)

    async def handle_server_answer(self, data, room: "Room"):
        answer = RTCSessionDescription(data)
        await self.pc.setRemoteDescription(answer)

    async def handle_message(self, message, room: "Room"):
        type = message.get("type")
        data = message.get("text")
        if type == Actions.DISCONNECT.value:
            await self.handle_disconnect(room)
            return 
        data = json.loads(data)
        if data["type"] == Actions.JOIN.value:
            await self.handle_join(data["payload"], room)
        elif data["type"] == Actions.LEAVE.value:
            await self.handle_leave(data["payload"], room)
        elif data["type"] == Actions.RELAY_SDP.value:
            await self.handle_relay_sdp(data["payload"], room)
        elif data["type"] == Actions.RELAY_ICE.value:
            await self.handle_relay_ice(data["payload"], room)
        elif data["type"] == Actions.NEW_MSG.value:
            await self.handle_new_message(data["payload"], room)
        elif data["type"] == Actions.STARTED_SCREEN_SHARING.value:
            await self.handle_started_screen_sharing(data["payload"], room)
        elif data["type"] == Actions.STOPPED_SCREEN_SHARING.value:
            await self.handle_stopped_screen_sharing(data["payload"], room)
        elif data["type"] == Actions.END_CALL.value:
            await self.handle_end_call(data["payload"], room)
        elif data["type"] == Actions.ENABLE_CAMERA.value:
            await self.handle_enable_camera(data["payload"], room)
        elif data["type"] == Actions.DISABLE_CAMERA.value:
            await self.handle_disable_camera(data["payload"], room)
        elif data["type"] == Actions.ENABLE_MICROPHONE.value:
            await self.handle_enable_microphone(data["payload"], room)
        elif data["type"] == Actions.DISABLE_MICROPHONE.value:
            await self.handle_disable_microphone(data["payload"], room)
        elif data["type"] == Actions.ROTATE.value:
            await self.handle_rotate(data["payload"], room)
        elif data["type"] == Actions.PING.value:
            await self.handle_ping()
        elif data["type"] == Actions.SERVER_OFFER.value:
            await self.handle_offer(data["payload"], room)
        elif data["type"] == Actions.SERVER_ICE.value:
            await self.handle_server_ice(data["payload"], room)
        elif data["type"] == Actions.SERVER_ANSWER.value:
            await self.handle_server_answer(data["payload"], room)

    async def close(self) -> None:
        try:
            await self.websocket.close()
        except RuntimeError:
            pass


class Room:
    def __init__(self, room_id: str | None, owner_id: str | None, is_group: bool = False) -> None:
        self.id = room_id or uuid4()
        self.clients = {}
        self.chat: Chat = Chat(session_id=self.id)
        self.owner_id = owner_id
        self.is_group = is_group

    def add_client(self, client: Client) -> None:
        self.clients[client.id] = client

    async def remove_client(self, client_id) -> None:
        if client_id in self.clients:
            del self.clients[client_id]
        #if len(self.clients.keys()) == 0:
        #   await rooms.delete_room(self.id)

    def get_clients(self) -> List[Client]:
        return self.clients.values()
    
    def get_client(self, client_id: str) -> Client:
        return self.clients[client_id]
    
    def get_client_by_uuid(self, client_id: str) -> Client:
        return self.clients[client_id]
    
    def get_owner(self) -> str | None:
        return self.owner_id
    
    async def send_chat_message(self, client_id: str, message: str) -> None:
        client = self.get_client_by_uuid(client_id=client_id)
        if client is None:
            return
        send_time = datetime.now()
        message_obj = Message(client_id=client_id, username=client.name, message=message, timestamp=send_time)
        await self.chat.send_message(message=message_obj)
        data = {
            "type": Actions.NEW_MSG.value,
            "payload": message_obj.__str__()
        }
        return data
    
    async def get_all_messages(self) -> None:
        messages = await self.chat.get_all_messages()
        data = {
            "type": Actions.CHAT_HISTORY.value,
            "payload": [message.__str__() for message in messages]
        }
        return data
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "clients": [client.to_dict() for client in self.clients.values()]
        }

    async def close(self) -> None:
        for client in list(self.clients.values()):
            await client.close()
        self.clients.clear()


class RoomsContainer:
    def __init__(self) -> None:
        self.rooms = {}

    def get_room(self, room_id: str) -> Optional[Room]:
        return self.rooms.get(room_id, None)

    def create_room(self, room_id: int, owner_id: str, is_group: bool = False) -> Room:
        room = self.get_room(room_id=room_id)
        if room is None:
            room = Room(room_id, owner_id, is_group)
            self.rooms[room.id] = room
        return room

    async def delete_room(self, room_id: str) -> None:
        room = self.get_room(room_id=room_id)
        if room is not None:
            await room.close()
            del self.rooms[room_id]

    def get_rooms_info(self) -> dict:
        return [room.to_dict() for room in self.rooms.values()]

    async def clear(self) -> None:
        for room in self.rooms.values():
            await self.delete_room(room_id=room.id)
        self.rooms.clear()


class ClientsContainer:
    def __init__(self) -> None:
        self.clients = {}

    def get_client(self, client_id: str) -> Optional[Client]:
        return self.clients.get(client_id)

    def create_client(self, client_id: str, name: Optional[str] = None, room_id: Optional[str] = None) -> Client:
        if room_id is not None:
            room = rooms.get_room(room_id=room_id)
        else:
            room = None
        client = Client(client_id=client_id, name=name, room=room)
        self.clients[client.id] = client
        return client

    async def delete_client(self, client_id: str) -> None:
        client = self.get_client(client_id=client_id)
        await client.close()
        del self.clients[client_id]

    async def clear(self) -> None:
        for client in self.clients.values():
            await self.delete_client(client.id)
        self.clients.clear()


rooms = RoomsContainer()
clients = ClientsContainer()
