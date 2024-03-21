import time

from apiflask import APIFlask, HTTPBasicAuth, Schema
from b2sdk.v2 import InMemoryAccountInfo
from dotenv import load_dotenv
from flask_cors import CORS
from flask_socketio import SocketIO
from marshmallow.fields import Nested, String

from api.websocket.handlers import register_handlers
from api.websocket.resources import SocketResources

load_dotenv()

info = InMemoryAccountInfo()

app = APIFlask(__name__, title="Transcribe API", version="0.1.0", spec_path="/openapi.yaml", docs_ui="rapidoc")
app.servers = [
    {
        'name': 'Production Server',
        'url': 'https://transcribe-api.lincolnnguyen.me'
    },
    {
        'name': 'Dev Server',
        'url': 'http://localhost:34204'
    },
]
auth = HTTPBasicAuth()
socketio = SocketIO(app, cors_allowed_origins="*")
register_handlers(socketio)

app.config["SPEC_FORMAT"] = "yaml"
app.config["LOCAL_SPEC_PATH"] = "openapi.yaml"
app.config["SYNC_LOCAL_SPEC"] = True
CORS(app, supports_credentials=False, origins="*", allow_headers="*", expose_headers="*")


class PingOut(Schema):
    socket_resources = Nested(SocketResources)
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
