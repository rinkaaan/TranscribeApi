WORKPLACE="$HOME/workplace/Transcribe"

(
  cd "$WORKPLACE/PythonUtils"
  pip install .
  rm -rf build
)
