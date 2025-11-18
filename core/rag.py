# core/rag.py
import os
import json
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
import faiss
from pdfminer.high_level import extract_text

EMBED_MODEL_NAME = "all-MiniLM-L6-v2"

class DocStore:
    def __init__(self, data_dir="data/docs", index_path="data/docs.index"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.index_path = index_path
        self.embedder = SentenceTransformer(EMBED_MODEL_NAME)
        self.texts = []     # list[str]
        self.metadatas = [] # list[dict]
        self.index = None
        if os.path.exists(index_path):
            self._load_index()
        else:
            self._build_empty_index()

    def _build_empty_index(self):
        dim = self.embedder.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(dim)

    def _load_index(self):
        # For simplicity, we rebuild index from files (safer for small projects)
        self._build_empty_index()
        self._load_texts_and_index()

    def _load_texts_and_index(self):
        self.texts = []
        self.metadatas = []
        for fname in os.listdir(self.data_dir):
            if not fname.lower().endswith(".pdf"):
                continue
            path = os.path.join(self.data_dir, fname)
            txt = extract_text(path)
            chunks = self._chunk_text(txt)
            for i, chunk in enumerate(chunks):
                self.texts.append(chunk)
                self.metadatas.append({"source": fname, "chunk": i})
        if self.texts:
            embeddings = self.embedder.encode(self.texts, convert_to_numpy=True)
            self.index.add(embeddings)

    def _chunk_text(self, text: str, chunk_size: int = 800) -> List[str]:
        # naive chunking by characters
        chunks = []
        for i in range(0, len(text), chunk_size):
            chunks.append(text[i:i+chunk_size])
        return chunks

    def index_all(self):
        # (re)build index
        self._build_empty_index()
        self._load_texts_and_index()

    def search(self, query: str, k: int = 5) -> List[Tuple[dict, str]]:
        if not self.texts:
            return []
        q_emb = self.embedder.encode([query], convert_to_numpy=True)
        D, I = self.index.search(q_emb, k)
        candidates = []
        for idx in I[0]:
            if idx < 0 or idx >= len(self.texts):
                continue
            candidates.append((self.metadatas[idx], self.texts[idx]))
        return candidates

if __name__ == "__main__":
    ds = DocStore()
    ds.index_all()
    print("Indexed docs:", len(ds.texts))
