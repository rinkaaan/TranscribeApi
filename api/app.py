import time

from apiflask import APIFlask, HTTPBasicAuth
from b2sdk.v2 import InMemoryAccountInfo
from dotenv import load_dotenv
from flask_cors import CORS
from flask_socketio import SocketIO

load_dotenv()

info = InMemoryAccountInfo()

app = APIFlask(__name__, title="Transcribe API", version="0.1.0", spec_path="/openapi.yaml", docs_ui="rapidoc")
auth = HTTPBasicAuth()
socketio = SocketIO(app, cors_allowed_origins="*")

app.config["SPEC_FORMAT"] = "yaml"
app.config["LOCAL_SPEC_PATH"] = "openapi.yaml"
app.config["SYNC_LOCAL_SPEC"] = True
CORS(app, supports_credentials=False, origins="*", allow_headers="*", expose_headers="*")


@socketio.on("connect")
def on_connect():
    print("Client connected!")


@app.get("/ping")
def ping():
    return "pong"


@app.before_request
def add_fake_delay():
    fake_delay = 0
    time.sleep(fake_delay)


if __name__ == "__main__":
    app.run(port=34204, debug=True)
