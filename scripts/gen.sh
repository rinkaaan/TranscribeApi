WORKPLACE="$HOME/workplace/Transcribe"
WORKSPACE="$WORKPLACE/TranscribeApi"

(
  cd "$WORKSPACE/api"
  flask spec --output openapi.yaml > /dev/null
)
