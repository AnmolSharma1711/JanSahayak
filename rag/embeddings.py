"""
RAG Embeddings Module
Uses HuggingFace sentence-transformers for CPU-based embeddings
"""

from langchain_community.embeddings import HuggingFaceEmbeddings
import os


def get_embeddings():
    """
    Returns HuggingFace embeddings model for CPU inference
    Model: sentence-transformers/all-MiniLM-L6-v2
    - Fast inference on CPU
    - 384-dimensional embeddings
    - Good for semantic search
    
    Note: On first run, downloads ~80MB model from HuggingFace
    """
    try:
        # Set cache directory to avoid permission issues on cloud platforms
        cache_dir = os.environ.get('HF_HOME', './hf_cache')
        
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            cache_folder=cache_dir
        )
    except Exception as e:
        print(f"⚠️  Failed to load embeddings model: {str(e)}")
        raise RuntimeError(f"Embeddings model loading failed: {str(e)}")
