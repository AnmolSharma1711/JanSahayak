"""
Exam Vectorstore Module
Builds and loads FAISS vectorstore for competitive exams
"""

import os
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from rag.embeddings import get_embeddings


def build_exam_vectorstore():
    """
    Reads all PDFs from data/exams_pdfs/ and builds FAISS index
    Run this once to initialize the vectorstore
    """
    documents = []
    folder = "data/exams_pdfs"
    
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created {folder}. Please add exam PDFs to this folder.")
        return

    pdf_files = [f for f in os.listdir(folder) if f.endswith(".pdf")]
    
    if not pdf_files:
        print(f"No PDF files found in {folder}. Please add exam PDFs.")
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
    
    os.makedirs("rag/exam_index", exist_ok=True)
    vectorstore.save_local("rag/exam_index")
    print("Exam vectorstore built successfully!")


def load_exam_vectorstore():
    """
    Loads pre-built exam vectorstore
    Returns FAISS vectorstore instance
    
    Raises:
        FileNotFoundError: If vectorstore files don't exist
        RuntimeError: If embeddings fail to load
    """
    if not os.path.exists("rag/exam_index/index.faiss"):
        raise FileNotFoundError(
            "Exam vectorstore not found at rag/exam_index/index.faiss. "
            "Run 'python init_embeddings.py' or build_exam_vectorstore() first."
        )
    
    print("📂 Loading exam vectorstore...")
    embeddings = get_embeddings()
    vectorstore = FAISS.load_local("rag/exam_index", embeddings, allow_dangerous_deserialization=True)
    print("✅ Exam vectorstore loaded successfully")
    return vectorstore
