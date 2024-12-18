import os
import asyncio
from datetime import datetime
from enum import Enum
from aiortc import RTCPeerConnection, MediaStreamTrack
from aiortc.contrib.media import MediaRecorder
import moviepy


class RecorderTypes(Enum):
    WEBCAM = "webcam"
    SCREEN = "screen"

class Recorder:
    def __init__(self, room_id: str, client_id: str, base_dir: str = "./recordings"):
        """
        Initialize the Recorder.
        
        :param room_id: ID of the room where the recording is taking place.
        :param client_id: ID of the client associated with the recording.
        :param base_dir: Base directory to store recording files.
        """
        self.room_id = room_id
        self.client_id = client_id
        self.base_dir = base_dir
        self.recorders = []  # List to hold track-specific MediaRecorder instances

        # Ensure the base directory exists
        self._ensure_directory()

    def _ensure_directory(self):
        """Ensure the recording directory exists."""
        room_path = os.path.join(self.base_dir, self.room_id)
        if not os.path.exists(room_path):
            os.makedirs(room_path)

    def setup(self):
        """Prepare the recorder (additional setup if needed)."""
        print(f"Recorder setup complete for room {self.room_id}, client {self.client_id}")

    def add_track(self, track):
        """
        Add a track to the recorder.
        
        :param track: The media track to be recorded.
        """
        if track.kind == "audio":
            file_path = os.path.join(self.base_dir, self.room_id, f"{self.client_id}_audio.wav")
        elif track.kind == "video":
            file_path = os.path.join(self.base_dir, self.room_id, f"{self.client_id}_video.mp4")
        else:
            print(f"Unsupported track type: {track.kind}")
            return

        recorder = MediaRecorder(file_path)
        recorder.addTrack(track)
        self.recorders.append(recorder)

        print(f"Added {track.kind} track to recording: {file_path}")

    async def start(self):
        """Start recording all tracks."""
        for recorder in self.recorders:
            await recorder.start()
        print("Recording started.")

    async def stop(self):
        """Stop recording all tracks."""
        for recorder in self.recorders:
            await recorder.stop()
        print("Recording stopped and files saved.")

    def cleanup(self):
        """Clean up resources and remove incomplete files if needed."""
        print("Recorder cleanup complete.")
