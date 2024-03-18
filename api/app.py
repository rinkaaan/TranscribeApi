import time

from apiflask import APIFlask, HTTPBasicAuth
from b2sdk.v2 import InMemoryAccountInfo
from dotenv import load_dotenv
from flask import session
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, emit, leave_room

load_dotenv()

info = InMemoryAccountInfo()

app = APIFlask(__name__, title="Transcribe API", version="0.1.0", spec_path="/openapi.yaml", docs_ui="rapidoc")
auth = HTTPBasicAuth()
socketio = SocketIO(app, cors_allowed_origins="*")

app.config["SPEC_FORMAT"] = "yaml"
app.config["LOCAL_SPEC_PATH"] = "openapi.yaml"
app.config["SYNC_LOCAL_SPEC"] = True
CORS(app, supports_credentials=False, origins="*", allow_headers="*", expose_headers="*")


class SocketTranscriptionPayload:
    def __init__(self, username: str, room: str, text: str, translation: str):
        self.username = username
        self.room = room
        self.text = text
        self.translation = translation


class SocketJoinLeavePayload:
    def __init__(self, username: str, room: str):
        self.username = username
        self.room = room


class SocketMessagePayload:
    def __init__(self, username: str, room: str, text: str):
        self.username = username
        self.room = room
        self.text = text


@socketio.on("join")
def on_join(data):
    data = SocketJoinLeavePayload(**data)
    session["username"] = data.username
    session["room"] = data.room
    join_room(data.room)
    payload = SocketMessagePayload("Server", data.room, f"{data.username} has joined the room")
    emit("message", vars(payload), to=data.room)


@socketio.on("disconnect")
def on_disconnect():
    payload = SocketMessagePayload("Server", session["room"], f"{session["username"]} has left the room")
    emit("message", vars(payload), to=session["room"])


@socketio.on("transcription")
def on_transcription(data):
    data = SocketTranscriptionPayload(**data)
    emit("transcription", vars(data), to=data.room)


@socketio.on("message")
def on_message(data):
    data = SocketMessagePayload(**data)
    emit("message", vars(data), to=data.room)


@socketio.on("leave")
def on_leave(data):
    data = SocketJoinLeavePayload(**data)
    leave_room(data.room)
    payload = SocketMessagePayload("Server", data.room, f"{data.username} has left the room")
    emit("message", vars(payload), to=data.room)


@app.get("/ping")
def ping():
    return "pong"


@app.before_request
def add_fake_delay():
    fake_delay = 0
    time.sleep(fake_delay)


if __name__ == "__main__":
    app.run(port=34204, debug=True)
