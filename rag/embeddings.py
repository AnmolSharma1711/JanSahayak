"""
RAG Embeddings Module
Uses HuggingFace sentence-transformers for CPU-based embeddings
"""

from langchain_community.embeddings import HuggingFaceEmbeddings


def get_embeddings():
    """
    Returns HuggingFace embeddings model for CPU inference
    Model: sentence-transformers/all-MiniLM-L6-v2
    - Fast inference on CPU
    - 384-dimensional embeddings
    - Good for semantic search
    """
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
