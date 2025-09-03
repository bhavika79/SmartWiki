import numpy as np
from sentence_transformers import SentenceTransformer
from utils.embedder import load_faiss_index
import json

emb_model = SentenceTransformer("all-MiniLM-L6-v2")
def retrieve_docs(query, index, metadata, top_k = 3):
  query_embeddings = emb_model.encode([query]).astype("float32")
  scores,indices = index.search(query_embeddings,top_k)
  context_chunks = []

  for idx in indices[0]:
    context_chunks.append(metadata[idx]["text"])
  return context_chunks

