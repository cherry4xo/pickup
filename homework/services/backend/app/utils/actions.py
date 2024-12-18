from enum import Enum


class Actions(Enum):
    JOIN = "join"
    LEAVE = "leave"
    YOUR_NAME = "your-name"
    SHARE_ROOMS = "share-rooms"
    ADD_PEER = "add-peer"
    REMOVE_PEER = "remove-peer"
    RELAY_SDP = "relay-sdp"
    RELAY_ICE = "relay-ice"
    ICE_CANDIDATE = "ice-candidate"
    SESSION_DESCRIPTION = "session-description"
    DISCONNECT = "websocket.disconnect"
    NEW_MSG = "new_msg"
    CHAT_HISTORY = "chat_history"
    STARTED_SCREEN_SHARING = "started-screen-sharing"
    STOPPED_SCREEN_SHARING = "stopped-screen-sharing"
    END_CALL = "end-call"
    OWNER = "owner"
    ENABLE_CAMERA = "enable-camera"
    DISABLE_CAMERA = "disable-camera"
    ENABLE_MICROPHONE = "enable-microphone"
    DISABLE_MICROPHONE = "disable-microphone"
    ROTATE = "rotate"
    PING = "ping"
    PONG = "pong"
    SERVER_OFFER = "server-offer"
    SERVER_ANSWER = "server-answer"
    SERVER_ICE = "server-ice"


class DeviceTypes(Enum):
    DESKTOP = "desktop"
    MOBILE = "mobile"