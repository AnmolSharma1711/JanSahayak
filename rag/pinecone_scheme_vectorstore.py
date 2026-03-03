"""
Pinecone-based Scheme Vectorstore Module
Uses Pinecone cloud vector database for scheme documents
"""

import os
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders import PyPDFLoader
from rag.embeddings import get_embeddings
from config import PINECONE_API_KEY, PINECONE_INDEX_NAME


def build_pinecone_scheme_vectorstore():
    """
    Reads all PDFs from data/schemes_pdfs/ and uploads to Pinecone
    Run this once to initialize the vectorstore
    """
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY not found in environment variables")
    
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

    print(f"Loaded {len(documents)} document chunks.")
    
    # Initialize Pinecone
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # Check if index exists, create if not
    existing_indexes = [index.name for index in pc.list_indexes()]
    
    if PINECONE_INDEX_NAME not in existing_indexes:
        print(f"Creating Pinecone index: {PINECONE_INDEX_NAME}")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=384,  # all-MiniLM-L6-v2 dimension
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        print("Index created! Waiting for initialization...")
        import time
        time.sleep(10)  # Wait for index to be ready
    
    print("Uploading documents to Pinecone...")
    embeddings = get_embeddings()
    
    # Upload to Pinecone with namespace for schemes
    vectorstore = PineconeVectorStore.from_documents(
        documents=documents,
        embedding=embeddings,
        index_name=PINECONE_INDEX_NAME,
        namespace="schemes"
    )
    
    print(f"✅ Successfully uploaded {len(documents)} documents to Pinecone!")
    return vectorstore


def load_pinecone_scheme_vectorstore():
    """
    Loads scheme vectorstore from Pinecone
    Returns PineconeVectorStore instance
    
    Raises:
        ValueError: If API key is missing
        Exception: If connection fails
    """
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY not found in environment variables")
    
    print("📂 Connecting to Pinecone scheme vectorstore...")
    
    embeddings = get_embeddings()
    
    vectorstore = PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        embedding=embeddings,
        namespace="schemes"
    )
    
    print("✅ Pinecone scheme vectorstore connected")
    return vectorstore
