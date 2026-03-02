# 🧠 JanSahayak - Multi-Agent Government Intelligence System

An intelligent multi-agent system for Indian government schemes and exam recommendations using LangChain, LangGraph, and Groq API.

## ✨ Now with Beautiful Web UI!

Access JanSahayak through a modern, intuitive web interface with real-time progress tracking, interactive forms, and beautiful visualizations.

**Quick Start:** `python app.py` → **http://localhost:5000**

![Modern UI](https://img.shields.io/badge/UI-Modern%20%26%20Beautiful-purple)
![Flask](https://img.shields.io/badge/Flask-Web%20App-green)
![Responsive](https://img.shields.io/badge/Design-Responsive-blue)

## 🎯 Features

- **User Profiling Agent**: Extracts structured user information
- **Scheme Recommendation Agent**: RAG-based scheme matching
- **Exam Recommendation Agent**: Competitive exam guidance
- **Web Search Agent**: Live government website search via Tavily
- **RAG Retrieval Agent**: Vector-based document search
- **Document Processing Agent**: PDF and image text extraction
- **Missed Benefits Calculator**: Estimates unclaimed benefits

## 🏗️ Architecture

```
User Input → Profiling Agent
              ↓
         ┌────────────────┐
         ↓                ↓
    Scheme Agent     Exam Agent
         ↓
    Benefit Agent
         ↓
    Final JSON Output
```

## 📦 Installation

1. Create virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure API keys:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Add government scheme and exam PDFs:
- Place scheme PDFs in `data/schemes_pdfs/`
- Place exam PDFs in `data/exams_pdfs/`

5. Build vector stores:
```bash
python -c "from rag.scheme_vectorstore import build_scheme_vectorstore; build_scheme_vectorstore()"
python -c "from rag.exam_vectorstore import build_exam_vectorstore; build_exam_vectorstore()"
```

## 🚀 Usage

### Web Interface (Recommended)

Start the Flask web application:

```bash
python app.py
```

Then open your browser and go to: **http://localhost:5000**

Features:
- Beautiful, modern UI
- Interactive form with examples
- Real-time progress tracking
- Results visualization
- Download reports
- View analysis history

### Command Line Interface

For batch processing or scripting:

```bash
python main.py
```

## 🔑 API Keys Required

- **Groq API**: https://console.groq.com/
- **Tavily API**: https://tavily.com/
- **HuggingFace Token**: https://huggingface.co/settings/tokens

## 📁 Project Structure

See code comments for detailed module documentation.

## 🎯 CPU-Only Deployment

This system runs entirely on CPU using:
- HuggingFace sentence-transformers for embeddings
- PyTorch CPU version
- FAISS CPU for vector search
- Groq API for LLM inference (no local GPU needed)
