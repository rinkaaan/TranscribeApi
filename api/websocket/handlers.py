from flask import session, request
from flask_socketio import join_room, emit, leave_room

from api.websocket.resources import JoinLeaveMessage, FinalTranscription, InterimTranscription


def register_handlers(socketio):
    @socketio.on("join")
    def on_join(payload):
        payload: JoinLeaveMessage = JoinLeaveMessage().load(payload)
        session["username"] = payload.username
        session["room"] = payload.room
        join_room(payload.room)
        response = {
            "username": "Server",
            "room": payload.room,
            "text": f"{payload.username} has joined the room"
        }

        room_connections = socketio.server.manager.rooms["/"][payload.room]
        session["id"] = request.sid
        # print(f"Room connections: {room_connections}")
        total_connections = len(room_connections)
        # print(f"Total connections: {total_connections}")

        emit("message", response, to=payload.room, include_self=total_connections > 1)

    @socketio.on("update_username")
    def on_update_username(new_username):
        session["username"] = new_username

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

    @socketio.on("final_transcription")
    def on_transcription(payload):
        payload: FinalTranscription = FinalTranscription().load(payload)
        payload.id = session["id"]
        payload.username = session["username"]
        payload.room = session["room"]
        # print(f"Transcription id: {payload.id}")
        response = FinalTranscription().dump(payload)
        emit("final_transcription", response, to=payload.room, include_self=False)

    @socketio.on("interim_transcription")
    def on_interim_transcription(payload):
        payload: InterimTranscription = InterimTranscription().load(payload)
        payload.id = session["id"]
        payload.username = session["username"]
        payload.room = session["room"]
        response = InterimTranscription().dump(payload)
        emit("interim_transcription", response, to=payload.room, include_self=False)

    @socketio.on("message")
    def on_message(payload):
        emit("message", payload, to=session["room"])

    @socketio.on("leave")
    def on_leave(payload):
        payload: JoinLeaveMessage = JoinLeaveMessage().load(payload)
        leave_room(payload.room)
        response = {
            "username": "Server",
            "room": payload.room,
            "text": f"{payload.username} has left the room"
        }
        emit("message", response, to=payload.room)
