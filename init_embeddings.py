"""
Pre-download and initialize embeddings model
Run this during deployment to ensure embeddings are ready
Uses FAISS for local vector storage
"""

import os
import sys


def download_embeddings():
    """Download HuggingFace embeddings model during build"""
    try:
        print("="*70)
        print("📦 Downloading HuggingFace Embeddings Model")
        print("="*70)
        
        # Import after requirements are installed
        import sys
        sys.path.insert(0, '.')
        from rag.embeddings import get_embeddings
        
        print(f"\n📂 Cache directory: {os.environ.get('HF_HOME', './hf_cache')}")
        print("🔄 Downloading sentence-transformers/all-MiniLM-L6-v2...")
        print("   (This is ~80MB and will be cached for future use)\n")
        
        # Initialize embeddings - this will download the model
        embeddings = get_embeddings()
        
        # Test the embeddings
        test_text = "Government welfare scheme for farmers"
        print("🧪 Testing embeddings...")
        _ = embeddings.embed_query(test_text)
        
        print("\n✅ Embeddings model downloaded and verified successfully!")
        print("="*70)
        return True
        
    except Exception as e:
        print(f"\n❌ Failed to download embeddings: {str(e)}")
        import traceback
        traceback.print_exc()
        print("="*70)
        return False


def build_exam_index_if_needed():
    """Build exam vectorstore if it doesn't exist"""
    try:
        if os.path.exists("rag/exam_index/index.faiss"):
            print("✅ Exam index already exists")
            return True
        
        print("\n⚠️  Exam index not found")
        
        # Check if we have exam PDFs
        exam_pdfs_dir = "data/exams_pdfs"
        if not os.path.exists(exam_pdfs_dir):
            print(f"   {exam_pdfs_dir} directory doesn't exist")
            print("   Exam recommendations will use web search only")
            return False
        
        pdf_files = [f for f in os.listdir(exam_pdfs_dir) if f.endswith('.pdf')]
        if not pdf_files:
            print(f"   No PDF files found in {exam_pdfs_dir}")
            print("   Exam recommendations will use web search only")
            return False
        
        print(f"\n🔨 Building exam index from {len(pdf_files)} PDF(s)...")
        import sys
        sys.path.insert(0, '.')
        from rag.exam_vectorstore import build_exam_vectorstore
        build_exam_vectorstore()
        print("✅ Exam index built successfully")
        return True
        
    except Exception as e:
        print(f"⚠️  Could not build exam index: {str(e)}")
        import traceback
        traceback.print_exc()
        print("   Exam recommendations will use web search only")
        return False


def verify_indexes():
    """Verify that vector store indexes are accessible"""
    print("\n" + "="*70)
    print("🔍 Verifying Vector Store Indexes (FAISS)")
    print("="*70)
    
    scheme_exists = os.path.exists("rag/scheme_index/index.faiss")
    exam_exists = os.path.exists("rag/exam_index/index.faiss")
    
    print(f"\n📊 Scheme Index: {'✅ Found' if scheme_exists else '❌ Not Found'}")
    if scheme_exists:
        size = os.path.getsize("rag/scheme_index/index.faiss") / (1024*1024)
        print(f"   Size: {size:.2f} MB")
    
    print(f"\n📚 Exam Index: {'✅ Found' if exam_exists else '❌ Not Found'}")
    if exam_exists:
        size = os.path.getsize("rag/exam_index/index.faiss") / (1024*1024)
        print(f"   Size: {size:.2f} MB")
    
    if not scheme_exists and not exam_exists:
        print("\n⚠️  No vector stores found!")
        print("   Application will use web search only mode")
    elif not scheme_exists:
        print("\n⚠️  Scheme index missing - only web search for schemes")
    elif not exam_exists:
        print("\n⚠️  Exam index missing - only web search for exams")
    else:
        print("\n✅ All vector stores ready!")
    
    print("="*70)


if __name__ == "__main__":
    print("\n🚀 JanSahayak - Initializing Embeddings and Indexes")
    print("📌 Mode: FAISS (Local Vector Database)\n")
    
    # Step 1: Download embeddings model
    embeddings_ok = download_embeddings()
    
    if not embeddings_ok:
        print("\n⚠️  WARNING: Embeddings download failed!")
        print("   Vector stores will not work. Application will use web search only.")
        sys.exit(1)
    
    # Step 2: Build exam index if needed
    build_exam_index_if_needed()
    
    # Step 3: Verify indexes
    verify_indexes()
    
    print("\n✅ Initialization complete!\n")
