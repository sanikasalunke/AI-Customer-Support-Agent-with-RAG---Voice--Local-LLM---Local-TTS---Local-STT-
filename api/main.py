# api/main.py
from fastapi import FastAPI, UploadFile, File, WebSocket, HTTPException
from fastapi.responses import FileResponse
import uvicorn
from core.agent import SupportAgent
from core.llm_loader import load_llm
from tools.stt_whisper import transcribe_audio_bytes
from tools.tts_coqui import synthesize_text_to_wav
import uuid, os

app = FastAPI(title="AI Customer Support Agent API")
llm = load_llm()
agent = SupportAgent(llm=llm)

@app.post("/session/start")
def start():
    sid = str(uuid.uuid4())
    agent.start_session(sid)
    return {"session_id": sid}

@app.post("/session/{session_id}/message")
def send_message(session_id: str, payload: dict):
    text = payload.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")
    return agent.add_user_message(session_id, text)

@app.post("/session/{session_id}/audio")
async def send_audio(session_id: str, file: UploadFile = File(...)):
    audio_bytes = await file.read()
    text = transcribe_audio_bytes(audio_bytes, format=file.filename.split(".")[-1])
    res = agent.add_user_message(session_id, text)
    # optionally produce tts
    wav_path = synthesize_text_to_wav(res["reply"])
    return {"transcript": text, "reply": res["reply"], "wav": wav_path}

@app.post("/session/{session_id}/save")
def save(session_id: str):
    return agent.save_chat(session_id)

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    agent.start_session(session_id)
    try:
        while True:
            data = await websocket.receive_text()
            resp = agent.add_user_message(session_id, data)
            # also send TTS file path if desired
            await websocket.send_text(resp["reply"])
    except Exception:
        await websocket.close()

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
