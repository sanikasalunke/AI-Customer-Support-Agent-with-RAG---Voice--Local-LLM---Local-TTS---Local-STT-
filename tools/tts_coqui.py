# tools/tts_coqui.py
from TTS.api import TTS
import os
import tempfile

# choose one of the installed TTS models (list models via TTS.list_models())
# Example: "tts_models/en/ljspeech/tacotron2-DDC" (model names vary)
TTS_MODEL = os.getenv("COQUI_TTS_MODEL", "tts_models/en/ljspeech/tacotron2-DDC")
tts = TTS(TTS_MODEL, progress_bar=False, gpu=False)

def synthesize_text_to_wav(text: str, out_path: str = None) -> str:
    out_path = out_path or tempfile.mktemp(suffix=".wav")
    tts.tts_to_file(text=text, file_path=out_path)
    return out_path
