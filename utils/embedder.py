from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import os
import json

emb_model = SentenceTransformer("all-MiniLM-L6-v2")

def build_faiss_index():
   with open("artifacts/chunks/final_chunks.json", "r", encoding="utf-8") as file:
    chunks = json.load(file)
   embeddings = []
   for chunk in chunks:
      vector = emb_model.encode(chunk["text"])
      embeddings.append({
          "doc_id": chunk["doc_id"],
          "chunk_id": chunk["chunk_id"],
          "embedding": vector.tolist(),
          "text": chunk["text"]
      })
   output_file = os.path.join("artifacts/embeddings", "final_embeddings.json")
   with open(output_file, "w", encoding="utf-8") as file:
      json.dump(embeddings, file, indent=2, ensure_ascii=False)
   vectors = [np.array(e["embedding"], dtype ="float32") for e in embeddings]
   metadata = [{"doc_id":e["doc_id"], "chunk_id": e["chunk_id"], "text":e["text"]} for e in embeddings]

   vectors = np.vstack(vectors)
   dim = vectors.shape[1]
   index = faiss.IndexFlatL2(dim)
   index.add(vectors)
   faiss.write_index(index,"artifacts/faiss/my_index.faiss")
   with open("artifacts/faiss/metadata.json", "w", encoding="utf-8") as file:
    json.dump(metadata, file, indent=2, ensure_ascii=False)
   print("Faiss index built successfully")

def load_faiss_index():
  index = faiss.read_index("artifacts/faiss/my_index.faiss")
  with open("artifacts/faiss/metadata.json", "r", encoding="utf-8") as file:
    metadata = json.load(file)
  return index, metadata




