# 🛎️ AI Customer Support Agent (RAG + Voice, Fully Local)

A **fully offline**, privacy-preserving **AI Customer Support System** powered by **local LLMs**, **RAG**, **voice input/output**, and a clean **Streamlit UI**.

This project acts as a complete customer-support automation agent capable of:

- understanding user questions  
- retrieving answers from product manuals / PDFs  
- generating multi-turn conversational responses  
- recommending and comparing products  
- responding via text **and** voice  

All computation runs **on-device**, using open-source models.

---

## 🚀 Project Overview

This system combines **Retrieval-Augmented Generation (RAG)**, **speech recognition**, **text-to-speech**, and **local LLM reasoning** to create an AI assistant that behaves like a human customer support representative.

You can ask the agent:

> “What’s the battery life of the X200 headset?”  
> “Compare model A and model B for gaming.”  
> “My device won’t turn on — what should I try?”  
> “Read the safety section from the manual.”

The agent will search your PDFs, embed relevant sections, reason using a local LLM, and reply — optionally with synthesized voice.

---

## 🌟 Features

### 🧠 Local LLM-Powered Reasoning
- Runs **Mistral 7B Instruct (GGUF)** using `llama-cpp-python`
- Multi-turn conversational memory  
- Handles troubleshooting, FAQs, product comparisons  

### 🔍 RAG Search Across PDFs & Manuals
- Index and query documents using **FAISS vector search**
- Automated chunking, embedding, and retrieval
- Greatly reduces hallucinations  

### 🎙️ Voice Input (STT)
- Microphone-based input  
- Speech-to-text using **Whisper Tiny** (fast + offline)

### 🔊 Voice Output (TTS)
- Synthesized audio responses using **Coqui TTS**
- Multiple voices supported  
- Enables “hands-free” mode  

### 🖥️ Streamlit UI
- Clean chat interface (text + voice)
- Document upload system  
- Saves session history  

### 🌐 FastAPI Backend
- `/chat` endpoint  
- `/voice` endpoint  
- `/recommend` endpoint  
- Connectable with apps, CRMs, support systems  

### 💾 Persistent Session Storage
- Saves embeddings, chat history, and RAG cache  

### 🔒 Fully Offline
- No cloud APIs  
- Enterprise and privacy-safe  

---

## 🧩 Tech Stack

| Component | Technology |
|----------|------------|
| **LLM** | Mistral 7B Instruct (GGUF) |
| **Vector DB** | FAISS |
| **STT** | Whisper Tiny |
| **TTS** | Coqui TTS |
| **Backend** | FastAPI |
| **Frontend** | Streamlit |
| **Embeddings** | Instructor-XL / all-MiniLM |
| **Model Loader** | llama-cpp-python |


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
