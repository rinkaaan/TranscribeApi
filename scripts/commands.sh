scp -r root@hetzner:/root/workplace/Transcribe/TranscribeApi/sqlite.db /Volumes/workplace/Transcribe/TranscribeApi/api/sqlite.db

scp -r /Volumes/workplace/Transcribe/TranscribeApi/api/sqlite.db root@hetzner:/root/workplace/Transcribe/TranscribeApi/sqlite.db
scp -r ~/cookies.txt root@hetzner:~/cookies.txt

ln -sf /Volumes/workplace/Transcribe/TranscribeApi/sqlite.db /Volumes/workplace/Transcribe/TranscribeApi/api/sqlite.db
