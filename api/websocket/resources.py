from apiflask import Schema
from marshmallow import post_load
from apiflask.fields import String, Nested


class BaseSchema(Schema):
    @post_load
    def make_object(self, data, **_kwargs):
        class_name = self.__class__.__name__
        return type(class_name, (object,), data)()


class FinalTranscription(BaseSchema):
    username = String()
    room = String()
    text = String()
    translation = String()
    id = String()


class InterimTranscription(BaseSchema):
    username = String()
    room = String()
    text = String()
    id = String()


class JoinLeaveMessage(BaseSchema):
    username = String()
    room = String()


class Message(BaseSchema):
    username = String()
    room = String()
    text = String()


class SocketResources(Schema):
    socket_transcription_payload = Nested(FinalTranscription)
    socket_join_leave_payload = Nested(JoinLeaveMessage)
    socket_message_payload = Nested(Message)
    socket_interim_transcription_payload = Nested(InterimTranscription)
