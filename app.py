

import streamlit as st
from utils.scraper import scrape_wiki, load_excel
from utils.chunks import chunk_text
from utils.embedder import build_faiss_index, load_faiss_index
from utils.retriever import retrieve_docs
from utils.llm import generate_answer
import pandas as pd


st.set_page_config(page_title = "SmartWiki", layout = "wide" )
st.title("SmartWiki - AI powered wiki assistant")
st.write("Upload links, scrape articles, chunk, embed and query using LLM's!")


#**************************************************************************************

st.subheader("Welcome to SmartWiki")
st.subheader("Step 1: Upload and Scrape Articles")
excel_file = st.file_uploader("Upload Excel File", type = ["xlsx"])


# excel_file = pd.read_excel("data/wiki_excel.xlsx")
# df = pd.read_excel(excel_file)
# if "url" not in df.columns:
#   raise ValueError("Excel file must have a column named 'url'")
# else:
#   urls = df['url'].tolist()

if excel_file is not None:
  if st.button("Scrape Links"):
    with st.spinner("Scraping in progress..."):
      urls = load_excel(excel_file)
      scrape_wiki(urls)
    st.success("Scraping completed!")
st.subheader("Step 2: Chunking articles")
if st.button("Run CHUNKING"):
  with st.spinner("Chunking in progress..."):
    chunk_text(500)
  st.success("Chunking completed!")
st.subheader("Step 3: Generate Embeddings and Store in FAISS")
if st.button("Run EMBEDDING"):
  with st.spinner("Embedding in progress..."):
    build_faiss_index()
  st.success("Embedding completed!")
st.subheader("Step 4: Ask AI from your knowledge base")
query = st.text_input("Enter your question:")
if st.button("Get Answer"):
  if query.strip():
    with st.spinner("Generating answer..."):
      index, metadata = load_faiss_index()
      context_chunks = retrieve_docs(query, index, metadata, top_k = 3)
      answer = generate_answer(query, context_chunks)
      st.write(answer)
  else:
    st.warning("Please enter a question")



#**************************************************************************************

# #sidebar navigation
# st.sidebar.title("Navigation")
# menu = st.radio("Go to:", ("Home", "Scraping", "Chunking"," Embedding", "Ask AI"))

# #Home
# if menu == "Home":
#   st.subheader("Welcome to SmartWiki")
#   st.markdown("""
#   -**Step 1: **Upload an Excel file with acolum 'urls'
#   -**Step 2:** Scrape articles
#   -**Step 3:** Chunk articles into smaller pieces
#   -**Step 4:** Generate embeddings + store in FAISS
#   -**Step 5:** Ask questions with AI!
#   """)


# #Scraping
# elif menu == "Scraping":
#   st.subheader("Step 1: Upload and Scrape Articles")
#   excel_file = st.file_uploader("Upload Excel File", type = "xlsx")
#   if excel_file is not None:
#     if st.button("Scrape Links"):
#       with st.spinner("Scraping in progress..."):
#         urls = load_excel(excel_file)
#         scrape_wiki(urls)
#       st.sucess("Scraping completed!")

# #chunking
# elif menu == "Chunking":
#   st.subheader("Step 2: Chunking articles")
#   if st.button("Run CHUNKING"):
#     with st.spinner("Chunking in progress..."):
#       chunk_text(500)
#     st.sucess("Chunking completed!")

# #Embedding
# elif menu == "Embedding":
#   st.subheader("Step 3: Generate Embeddings and Store in FAISS")
#   if st.button("Run EMBEDDING"):
#     with st.spinner("Embedding in progress..."):
#       build_faiss_index()
#     st.sucess("Embedding completed!")

# #retriver
# elif menu == "Ask AI":
#   st.subheader("Step 4: Ask AI from your knowledge base")
#   query = st.text_input("Enter your question:")
#   if st.button("Get Answer"):
#     if query.strip():
#       with st.spinner("Generating answer..."):
#         index, metadata = load_faiss_index()
#         context_chunks = retrieve_docs(query, index, metadata, top_k = 3)
#         answer = generate_answer(query, context_chunks)
#         st.write(answer)

#     else:
#       st.warning("Please enter a question")

