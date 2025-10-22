import os, json, numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class BimpeKB:
    def __init__(self, kb_path: str):
        self.kb_path = kb_path
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.docs = []
        self.emb = None
        self._load()

    def _load(self):
        with open(self.kb_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.docs = data.get("docs", [])
        corpus = [d["title"] + " — " + d["content"] for d in self.docs]
        self.emb = self.model.encode(corpus, normalize_embeddings=True)

    def search(self, query: str, k: int = 4):
        q_emb = self.model.encode([query], normalize_embeddings=True)
        sims = cosine_similarity(q_emb, self.emb)[0]
        idx = np.argsort(-sims)[:k]
        results = []
        for i in idx:
            d = self.docs[i]
            results.append({
                "id": d["id"], "title": d["title"],
                "content": d["content"], "score": float(sims[i]),
                "qa_prompts": d.get("qa_prompts", [])
            })
        return results
