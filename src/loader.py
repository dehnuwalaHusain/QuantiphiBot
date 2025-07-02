import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

DATA_DIR = "../data"
INDEX_ROOT = "vector_store"

def build_indexes():
    embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

    for file in os.listdir(DATA_DIR):
        if not file.endswith(".pdf"):
            continue

        company = file.replace(".pdf", "")
        loader = PyPDFLoader(os.path.join(DATA_DIR, file))
        docs = loader.load()
        for d in docs:
            d.metadata["company"] = company
        
        print(docs)
        chunks = splitter.split_documents(docs)
        index_path = os.path.join(INDEX_ROOT, company)

        os.makedirs(index_path, exist_ok=True)
        db = FAISS.from_documents(chunks, embedder)
        db.save_local(index_path)
        print(f"Indexed {company} information into {len(chunks)} chunks")

if __name__ == "__main__":
    build_indexes()
