"""
Unified Vector Store Loader
Automatically loads the correct vectorstore based on configuration
Supports both FAISS (local) and Pinecone (cloud) modes
"""

from config import VECTOR_STORE_MODE, PINECONE_API_KEY
import os


def load_scheme_vectorstore():
    """
    Load scheme vectorstore based on configured mode
    Returns vectorstore instance (FAISS or Pinecone)
    """
    mode = VECTOR_STORE_MODE.lower()
    
    if mode == "pinecone":
        # Use Pinecone cloud vectorstore
        if not PINECONE_API_KEY:
            print("⚠️  Pinecone API key not found, falling back to FAISS")
            mode = "faiss"
        else:
            try:
                from rag.pinecone_scheme_vectorstore import load_pinecone_scheme_vectorstore
                return load_pinecone_scheme_vectorstore()
            except Exception as e:
                print(f"⚠️  Failed to load Pinecone vectorstore: {str(e)}")
                print("   Falling back to FAISS...")
                mode = "faiss"
    
    if mode == "faiss":
        # Use local FAISS vectorstore
        from rag.scheme_vectorstore import load_scheme_vectorstore as load_faiss
        return load_faiss()
    
    raise ValueError(f"Unknown VECTOR_STORE_MODE: {VECTOR_STORE_MODE}")


def load_exam_vectorstore():
    """
    Load exam vectorstore based on configured mode
    Returns vectorstore instance (FAISS or Pinecone)
    """
    mode = VECTOR_STORE_MODE.lower()
    
    if mode == "pinecone":
        # Use Pinecone cloud vectorstore
        if not PINECONE_API_KEY:
            print("⚠️  Pinecone API key not found, falling back to FAISS")
            mode = "faiss"
        else:
            try:
                from rag.pinecone_exam_vectorstore import load_pinecone_exam_vectorstore
                return load_pinecone_exam_vectorstore()
            except Exception as e:
                print(f"⚠️  Failed to load Pinecone vectorstore: {str(e)}")
                print("   Falling back to FAISS...")
                mode = "faiss"
    
    if mode == "faiss":
        # Use local FAISS vectorstore
        from rag.exam_vectorstore import load_exam_vectorstore as load_faiss
        return load_faiss()
    
    raise ValueError(f"Unknown VECTOR_STORE_MODE: {VECTOR_STORE_MODE}")


def get_vectorstore_info():
    """Get information about current vectorstore configuration"""
    mode = VECTOR_STORE_MODE.lower()
    
    info = {
        "mode": mode,
        "scheme_available": False,
        "exam_available": False
    }
    
    if mode == "pinecone":
        info["scheme_available"] = bool(PINECONE_API_KEY)
        info["exam_available"] = bool(PINECONE_API_KEY)
    else:
        info["scheme_available"] = os.path.exists("rag/scheme_index/index.faiss")
        info["exam_available"] = os.path.exists("rag/exam_index/index.faiss")
    
    return info
