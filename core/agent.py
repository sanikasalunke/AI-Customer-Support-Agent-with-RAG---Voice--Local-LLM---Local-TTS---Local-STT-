# core/agent.py
from typing import List, Dict
from core.llm_loader import load_llm
from core.rag import DocStore

class SupportAgent:
    def __init__(self, llm=None, docstore=None):
        self.llm = llm or load_llm()
        self.docstore = docstore or DocStore()
        self.sessions = {}  # session_id -> {"history":[(user,bot)], "context": {} }

    def start_session(self, session_id: str):
        self.sessions[session_id] = {"history": [], "context": {}}
        return {"session_id": session_id}

    def add_user_message(self, session_id: str, message: str):
        session = self.sessions.setdefault(session_id, {"history": [], "context": {}})
        session["history"].append(("user", message))
        return self._respond(session_id, message)

    def _build_prompt(self, session_id: str, user_message: str) -> str:
        session = self.sessions[session_id]
        history = session["history"][-6:]  # last 6 turns
        hist_text = "\n".join([f"{s}: {m}" for s,m in history])
        # RAG retrieval
        retrieved = self.docstore.search(user_message, k=3)
        retrieved_text = "\n---\n".join([f"Source: {md['source']}\n{txt[:800]}" for md, txt in retrieved])
        prompt = f"""You are a helpful customer support assistant with product knowledge.
User message: {user_message}

Relevant documents:
{retrieved_text}

Conversation history:
{hist_text}

Task: Provide a helpful, concise, multi-turn support response. If the user asks for product recommendation ask clarifying q's, otherwise answer using retrieved docs and common-sense.
"""
        return prompt

    def _respond(self, session_id: str, user_message: str) -> Dict:
        prompt = self._build_prompt(session_id, user_message)
        answer = self.llm.generate(prompt, max_tokens=400)
        # store bot response
        self.sessions[session_id]["history"].append(("bot", answer))
        return {"reply": answer, "session_id": session_id}

    def save_chat(self, session_id: str, path="data/chat_sessions.json"):
        import json, os
        os.makedirs("data", exist_ok=True)
        session = self.sessions.get(session_id)
        if not session:
            return {"error": "session not found"}
        saved = {"session_id": session_id, "history": session["history"]}
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                d = json.load(f)
        else:
            d = []
        d.append(saved)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)
        return {"status": "saved"}
