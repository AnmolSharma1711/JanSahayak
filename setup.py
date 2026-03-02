"""
Setup Utility Script
Helps in initial setup and vectorstore building
"""

import os
import sys


def check_dependencies():
    """Check if all required packages are installed"""
    print("Checking dependencies...")
    
    required_packages = [
        'langchain',
        'langgraph',
        'langchain_groq',
        'tavily',
        'faiss',
        'transformers',
        'sentence_transformers',
        'pypdf',
        'pytesseract',
        'PIL',
        'torch',
        'dotenv'
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                __import__('PIL')
            elif package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - NOT FOUND")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies installed!")
    return True


def check_env_file():
    """Check if .env file exists and has required keys"""
    print("\nChecking environment configuration...")
    
    if not os.path.exists('.env'):
        print("  ❌ .env file not found")
        print("  → Copy .env.example to .env and add your API keys")
        return False
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_keys = ['GROQ_API_KEY', 'TAVILY_API_KEY']
    missing = []
    
    for key in required_keys:
        value = os.getenv(key)
        if not value or value.startswith('your_'):
            print(f"  ❌ {key} - NOT CONFIGURED")
            missing.append(key)
        else:
            print(f"  ✅ {key}")
    
    if missing:
        print(f"\n⚠️ Missing API keys: {', '.join(missing)}")
        print("Edit .env file and add your API keys")
        return False
    
    print("\n✅ Environment configured!")
    return True


def check_pdf_data():
    """Check if PDF data is available"""
    print("\nChecking PDF data...")
    
    schemes_folder = "data/schemes_pdfs"
    exams_folder = "data/exams_pdfs"
    
    scheme_pdfs = [f for f in os.listdir(schemes_folder) if f.endswith('.pdf')] if os.path.exists(schemes_folder) else []
    exam_pdfs = [f for f in os.listdir(exams_folder) if f.endswith('.pdf')] if os.path.exists(exams_folder) else []
    
    print(f"  Scheme PDFs: {len(scheme_pdfs)} files")
    print(f"  Exam PDFs: {len(exam_pdfs)} files")
    
    if len(scheme_pdfs) == 0:
        print("\n  ⚠️ No scheme PDFs found in data/schemes_pdfs/")
        print("  Add government scheme PDFs to enable scheme recommendations")
    
    if len(exam_pdfs) == 0:
        print("\n  ⚠️ No exam PDFs found in data/exams_pdfs/")
        print("  Add competitive exam PDFs to enable exam recommendations")
    
    return len(scheme_pdfs) > 0 or len(exam_pdfs) > 0


def build_vectorstores():
    """Build vectorstores from PDFs"""
    print("\n" + "="*70)
    print("Building Vectorstores")
    print("="*70)
    
    # Build scheme vectorstore
    print("\n📚 Building Scheme Vectorstore...")
    try:
        from rag.scheme_vectorstore import build_scheme_vectorstore
        build_scheme_vectorstore()
    except Exception as e:
        print(f"❌ Error building scheme vectorstore: {str(e)}")
    
    # Build exam vectorstore
    print("\n📚 Building Exam Vectorstore...")
    try:
        from rag.exam_vectorstore import build_exam_vectorstore
        build_exam_vectorstore()
    except Exception as e:
        print(f"❌ Error building exam vectorstore: {str(e)}")
    
    print("\n" + "="*70)
    print("✅ Vectorstore building complete!")
    print("="*70)


def setup_wizard():
    """Interactive setup wizard"""
    print("\n" + "="*70)
    print("🚀 JANSAHAYAK SETUP WIZARD")
    print("="*70)
    
    # Step 1: Check dependencies
    print("\n[1/4] Checking Dependencies")
    print("-" * 70)
    deps_ok = check_dependencies()
    
    if not deps_ok:
        print("\n❌ Please install missing dependencies first")
        print("Run: pip install -r requirements.txt")
        return
    
    # Step 2: Check environment
    print("\n[2/4] Checking Environment Configuration")
    print("-" * 70)
    env_ok = check_env_file()
    
    if not env_ok:
        print("\n❌ Please configure your .env file first")
        return
    
    # Step 3: Check PDF data
    print("\n[3/4] Checking PDF Data")
    print("-" * 70)
    data_ok = check_pdf_data()
    
    if not data_ok:
        print("\n⚠️ No PDF data found. System will work with limited functionality.")
        cont = input("\nContinue anyway? (yes/no): ")
        if cont.lower() not in ['yes', 'y']:
            print("\nPlease add PDF files to data/ directories and run setup again.")
            return
    
    # Step 4: Build vectorstores
    print("\n[4/4] Building Vectorstores")
    print("-" * 70)
    
    if data_ok:
        build = input("\nBuild vectorstores now? (yes/no): ")
        if build.lower() in ['yes', 'y']:
            build_vectorstores()
        else:
            print("\n⚠️ Remember to build vectorstores before running the system!")
            print("Run: python setup.py --build-vectorstores")
    
    print("\n" + "="*70)
    print("✅ SETUP COMPLETE!")
    print("="*70)
    print("\nYou can now run the system:")
    print("  python main.py")
    print("\nFor help:")
    print("  python main.py --help")


def main():
    """Main setup function"""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--build-vectorstores':
            build_vectorstores()
        elif sys.argv[1] == '--check':
            check_dependencies()
            check_env_file()
            check_pdf_data()
        else:
            print("Usage:")
            print("  python setup.py                 # Run setup wizard")
            print("  python setup.py --check         # Check configuration")
            print("  python setup.py --build-vectorstores  # Build vectorstores")
    else:
        setup_wizard()


if __name__ == "__main__":
    main()
