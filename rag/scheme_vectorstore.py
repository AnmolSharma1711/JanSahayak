"""
Scheme Vectorstore Module
Builds and loads FAISS vectorstore for government schemes
"""

import os
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from rag.embeddings import get_embeddings


def build_scheme_vectorstore():
    """
    Reads all PDFs from data/schemes_pdfs/ and builds FAISS index
    Run this once to initialize the vectorstore
    """
    documents = []
    folder = "data/schemes_pdfs"
    
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created {folder}. Please add scheme PDFs to this folder.")
        return

    pdf_files = [f for f in os.listdir(folder) if f.endswith(".pdf")]
    
    if not pdf_files:
        print(f"No PDF files found in {folder}. Please add scheme PDFs.")
        return

    for file in pdf_files:
        print(f"Processing {file}...")
        loader = PyPDFLoader(os.path.join(folder, file))
        documents.extend(loader.load())

    if not documents:
        print("No documents extracted. Check PDF files.")
        return

    print(f"Loaded {len(documents)} document chunks. Building vectorstore...")
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    os.makedirs("rag/scheme_index", exist_ok=True)
    vectorstore.save_local("rag/scheme_index")
    print("Scheme vectorstore built successfully!")


def load_scheme_vectorstore():
    """
    Loads pre-built scheme vectorstore
    Returns FAISS vectorstore instance
    """
    embeddings = get_embeddings()
    
    if not os.path.exists("rag/scheme_index"):
        raise FileNotFoundError(
            "Scheme vectorstore not found. Run build_scheme_vectorstore() first."
        )
    
    return FAISS.load_local("rag/scheme_index", embeddings, allow_dangerous_deserialization=True)
