"""
Pre-download and initialize embeddings model
Run this during deployment to ensure embeddings are ready
Supports both FAISS (local) and Pinecone (cloud) vector stores
"""

import os
import sys
import argparse


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


def build_pinecone_indexes():
    """Build Pinecone vectorstores by uploading documents"""
    try:
        print("\n" + "="*70)
        print("☁️  Building Pinecone Vector Stores")
        print("="*70)
        
        import sys
        sys.path.insert(0, '.')
        from config import PINECONE_API_KEY, PINECONE_INDEX_NAME
        
        if not PINECONE_API_KEY:
            print("\n❌ PINECONE_API_KEY not found in environment variables")
            print("   Please set PINECONE_API_KEY in .env file")
            return False
        
        print(f"\n📌 Using Pinecone index: {PINECONE_INDEX_NAME}")
        
        # Build scheme vectorstore
        print("\n📊 Processing Scheme Documents...")
        from rag.pinecone_scheme_vectorstore import build_pinecone_scheme_vectorstore
        
        scheme_pdfs_dir = "data/schemes_pdfs"
        if os.path.exists(scheme_pdfs_dir):
            pdf_files = [f for f in os.listdir(scheme_pdfs_dir) if f.endswith('.pdf')]
            if pdf_files:
                print(f"   Found {len(pdf_files)} scheme PDF(s)")
                build_pinecone_scheme_vectorstore()
            else:
                print(f"   ⚠️  No PDFs in {scheme_pdfs_dir}")
        else:
            print(f"   ⚠️  Directory {scheme_pdfs_dir} not found")
        
        # Build exam vectorstore
        print("\n📚 Processing Exam Documents...")
        from rag.pinecone_exam_vectorstore import build_pinecone_exam_vectorstore
        
        exam_pdfs_dir = "data/exams_pdfs"
        if os.path.exists(exam_pdfs_dir):
            pdf_files = [f for f in os.listdir(exam_pdfs_dir) if f.endswith('.pdf')]
            if pdf_files:
                print(f"   Found {len(pdf_files)} exam PDF(s)")
                build_pinecone_exam_vectorstore()
            else:
                print(f"   ⚠️  No PDFs in {exam_pdfs_dir}")
        else:
            print(f"   ⚠️  Directory {exam_pdfs_dir} not found")
        
        print("\n" + "="*70)
        print("✅ Pinecone vector stores built successfully!")
        print("="*70)
        return True
        
    except Exception as e:
        print(f"\n❌ Failed to build Pinecone indexes: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def build_exam_index_if_needed():
    """Build exam vectorstore if it doesn't exist (FAISS mode)"""
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


def verify_indexes(mode="faiss"):
    """Verify that vector store indexes are accessible"""
    print("\n" + "="*70)
    print("🔍 Verifying Vector Store Indexes")
    print("="*70)
    
    if mode == "pinecone":
        print("\n☁️  Mode: Pinecone (Cloud Vector Database)")
        try:
            from config import PINECONE_API_KEY, PINECONE_INDEX_NAME
            if PINECONE_API_KEY:
                print(f"✅ Pinecone API Key: Found")
                print(f"✅ Index Name: {PINECONE_INDEX_NAME}")
                print("\n💡 Documents will be retrieved from Pinecone cloud")
            else:
                print("❌ Pinecone API Key: Not Found")
                print("   Set PINECONE_API_KEY in environment variables")
        except Exception as e:
            print(f"❌ Error checking Pinecone config: {str(e)}")
    else:
        print("\n💾 Mode: FAISS (Local Vector Database)")
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
    parser = argparse.ArgumentParser(description='Initialize embeddings and vector stores')
    parser.add_argument('--pinecone', action='store_true', 
                       help='Use Pinecone cloud vector database (recommended for deployment)')
    parser.add_argument('--faiss', action='store_true', 
                       help='Use FAISS local vector database (default)')
    
    args = parser.parse_args()
    
    # Determine mode
    if args.pinecone:
        mode = "pinecone"
    else:
        mode = "faiss"
    
    print("\n🚀 JanSahayak - Initializing Embeddings and Indexes")
    print(f"📌 Mode: {mode.upper()}\n")
    
    # Step 1: Download embeddings model
    embeddings_ok = download_embeddings()
    
    if not embeddings_ok:
        print("\n⚠️  WARNING: Embeddings download failed!")
        print("   Vector stores will not work. Application will use web search only.")
        sys.exit(1)
    
    # Step 2: Build indexes based on mode
    if mode == "pinecone":
        success = build_pinecone_indexes()
        if not success:
            print("\n⚠️  Pinecone setup incomplete. Check errors above.")
            sys.exit(1)
    else:
        # FAISS mode - build exam index if needed
        build_exam_index_if_needed()
    
    # Step 3: Verify indexes
    verify_indexes(mode)
    
    print("\n✅ Initialization complete!\n")
