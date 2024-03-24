source ~/startup.sh
WORKPLACE="$HOME/workplace/Transcribe"

WORKSPACE="$WORKPLACE/TranscribeApi"
(
  cd "$WORKSPACE"
  rsync-project Transcribe
  ssh root@hetzner "pm2 restart api-transcribe"
)
