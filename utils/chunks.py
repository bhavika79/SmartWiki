import nltk
from nltk.tokenize import sent_tokenize
nltk.download("punkt_tab", quiet = True)
import json
import os

def chunk_text(chunk_size):
  all_chunks = []
  for file_name in os.listdir("data/raw"):
    if file_name.endswith(".txt"):
      doc_id = file_name.replace(".txt", "")
      input_file = os.path.join("data/raw", file_name)
      with open(input_file, "r", encoding="utf-8") as file:
        text = file.read()
      sentences = sent_tokenize(text)
      chunks = []
      current_chunk = ""
      for s in sentences:
        if len(current_chunk)+ len(s)<=chunk_size:
          current_chunk += s+" "
        else:
          if current_chunk.strip():
            chunks.append(current_chunk.strip())
            current_chunk = s+" "

      if current_chunk.strip():
        chunks.append(current_chunk.strip())
      for i, chunk in enumerate(chunks):
              all_chunks.append({
                "doc_id": doc_id,
                "chunk_id": i,
                "text": chunk
              })
  output_file = os.path.join("artifacts/chunks", "final_chunks.json")
  with open(output_file, "w", encoding="utf-8") as file:
    json.dump(all_chunks, file, indent=2, ensure_ascii = False)

# def save_chunks(all_chunks, output_file):
#   with open(output_file, "w", encoding="utf-8") as file:
#     json.dump(all_chunks, file, indent=2, ensure_ascii = False)

# all_chunks = []
# for file_name in os.listdir("data/raw"):
#   if file_name.endswith(".txt"):
#     doc_id = file_name.replace(".txt", "")
#     input_file = os.path.join("data/raw", file_name)
#     with open(input_file, "r", encoding="utf-8") as file:
#       text = file.read()
#     chunks = chunk_text(text, 500)
#     for i, chunk in enumerate(chunks):
#       all_chunks.append({
#         "doc_id": doc_id,
#         "chunk_id": i,
#         "text": chunk
#       })
# output_file = os.path.join("artifacts/chunks", "final_chunks.json")
# save_chunks(all_chunks, output_file)
