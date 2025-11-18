# core/llm_loader.py
from typing import Optional
try:
    from llama_cpp import Llama
except Exception as e:
    Llama = None
    # raise at runtime if missing

class LLM:
    def __init__(self, model_path: str = "data/models/mistral-7b-instruct.gguf",
                 n_ctx: int = 4096, n_threads: int = 4, temp: float = 0.2):
        if Llama is None:
            raise RuntimeError("llama_cpp not installed. Install llama-cpp-python or adapt loader.")
        self.model = Llama(model_path=model_path, n_ctx=n_ctx, n_threads=n_threads)
        self.temp = temp

    def generate(self, prompt: str, max_tokens: int = 512) -> str:
        resp = self.model.create(prompt=prompt, max_tokens=max_tokens, temperature=self.temp)
        return resp['choices'][0]['text'].strip()

def load_llm(model_path: str = None) -> LLM:
    model_path = model_path or "data/models/mistral-7b-instruct.gguf"
    return LLM(model_path=model_path)
    