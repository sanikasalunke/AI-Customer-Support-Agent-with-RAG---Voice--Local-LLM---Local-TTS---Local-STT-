# AI Customer Support Agent (RAG + Voice)

Local, privacy-first customer support assistant:
- Local LLM (Mistral 7B GGUF via llama-cpp-python)
- FAISS vector search over PDFs/manuals
- Local STT: Whisper (tiny)
- Local TTS: Coqui TTS
- FastAPI backend + Streamlit demo UI
- Multi-turn chat, product recommendations, FAQ lookup, save sessions

## Quickstart (local)
1. Install deps:
   pip install -r requirements.txt
2. Place GGUF model: data/models/mistral-7b-instruct.gguf
3. Index docs: python -m tools.pdf_indexer
4. Run API:
   uvicorn api.main:app --reload --port 8000
5. Run UI:
   streamlit run ui/app.py
