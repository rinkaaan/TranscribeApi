import time

from apiflask import APIFlask, HTTPBasicAuth, Schema
from apiflask.fields import String, Nested
from b2sdk.v2 import InMemoryAccountInfo
from dotenv import load_dotenv
from flask import session
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, emit, leave_room
from marshmallow import post_load

load_dotenv()

info = InMemoryAccountInfo()

app = APIFlask(__name__, title="Transcribe API", version="0.1.0", spec_path="/openapi.yaml", docs_ui="rapidoc")
auth = HTTPBasicAuth()
socketio = SocketIO(app, cors_allowed_origins="*")

app.config["SPEC_FORMAT"] = "yaml"
app.config["LOCAL_SPEC_PATH"] = "openapi.yaml"
app.config["SYNC_LOCAL_SPEC"] = True
CORS(app, supports_credentials=False, origins="*", allow_headers="*", expose_headers="*")


class BaseSchema(Schema):
    @post_load
    def make_object(self, data, **_kwargs):
        class_name = self.__class__.__name__
        return type(class_name, (object,), data)()


class SocketTranscriptionPayload(BaseSchema):
    username = String()
    room = String()
    text = String()
    translation = String()


class SocketJoinLeavePayload(BaseSchema):
    username = String()
    room = String()


class SocketMessagePayload(BaseSchema):
    username = String()
    room = String()
    text = String()


@socketio.on("join")
def on_join(payload):
    payload = SocketJoinLeavePayload().load(payload)
    session["username"] = payload.username
    session["room"] = payload.room
    join_room(payload.room)
    response = {
        "username": "Server",
        "room": payload.room,
        "text": f"{payload.username} has joined the room"
    }
    emit("message", response, to=payload.room)


@socketio.on("disconnect")
def on_disconnect():
    if "username" not in session:
        return
    response = {
        "username": "Server",
        "room": session["room"],
        "text": f"{session['username']} has left the room"
    }
    emit("message", response, to=session["room"])


@socketio.on("transcription")
def on_transcription(payload):
    emit("transcription", payload, to=payload["room"])


@socketio.on("message")
def on_message(payload):
    emit("message", payload, to=payload["room"])


@socketio.on("leave")
def on_leave(payload):
    payload = SocketJoinLeavePayload().load(payload)
    leave_room(payload.room)
    response = {
        "username": "Server",
        "room": payload.room,
        "text": f"{payload.username} has left the room"
    }
    emit("message", response, to=payload.room)


class PingOut(Schema):
    socket_transcription_payload = Nested(SocketTranscriptionPayload)
    socket_join_leave_payload = Nested(SocketJoinLeavePayload)
    socket_message_payload = Nested(SocketMessagePayload)
    message = String()


@app.get("/ping")
@app.output(PingOut)
def ping():
    return {
        "message": "pong"
    }


@app.before_request
def add_fake_delay():
    fake_delay = 0
    time.sleep(fake_delay)


if __name__ == "__main__":
    app.run(port=34204, debug=True)
