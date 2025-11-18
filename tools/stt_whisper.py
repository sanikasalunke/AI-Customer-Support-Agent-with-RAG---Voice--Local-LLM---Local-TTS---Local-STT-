# tools/stt_whisper.py
import tempfile
import whisper
import os

model = whisper.load_model("tiny")  # local tiny model; downloads weights on first run

def transcribe_audio_bytes(audio_bytes: bytes, format: str = "wav") -> str:
    # write to temp file
    with tempfile.NamedTemporaryFile(suffix=f".{format}", delete=False) as tf:
        tf.write(audio_bytes)
        tf.flush()
        tmp_path = tf.name
    result = model.transcribe(tmp_path)
    text = result.get("text", "")
    try:
        os.remove(tmp_path)
    except:
        pass
    return text
