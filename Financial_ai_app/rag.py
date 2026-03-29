from sentence_transformers import SentenceTransformer, util
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

index = None
texts = []
embeddings_store = []

def chunk_text(text):
    size = 500
    return [text[i:i+size] for i in range(0, len(text), size)]

def add_chunks(chunks):
    global index, texts, embeddings_store

    embeddings = model.encode(chunks).astype("float32")

    if index is None:
        index = faiss.IndexFlatL2(embeddings.shape[1])

    index.add(embeddings)

    texts.extend(chunks)
    embeddings_store.extend(embeddings)

def rerank(query, candidates, candidate_embeddings):
    query_emb = model.encode(query)

    scores = []
    for emb in candidate_embeddings:
        score = util.cos_sim(query_emb, emb)
        scores.append(score.item())

    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    return [x[0] for x in ranked]

def search(query):
    global index, texts, embeddings_store

    if index is None:
        return []

    q = model.encode([query]).astype("float32")
    D, I = index.search(q, k=20)

    candidates = []
    candidate_embeddings = []

    for idx in I[0]:
        if idx < len(texts):
            candidates.append(texts[idx])
            candidate_embeddings.append(embeddings_store[idx])

    reranked = rerank(query, candidates, candidate_embeddings)

    return reranked[:5]