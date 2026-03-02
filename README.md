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

## 🌐 Deployment

Deploy JanSahayak to the cloud using one of these platforms:

### Render (Recommended - Easiest)

1. Fork/push repository to GitHub
2. Create account at [render.com](https://render.com)
3. Click "New +" → "Blueprint"
4. Connect your repository
5. Render auto-detects `render.yaml` configuration
6. Add environment variables in dashboard:
   - `GROQ_API_KEY`
   - `TAVILY_API_KEY`
   - `HF_TOKEN`
7. Click "Apply" - your app will be live in minutes!

**Cost**: Free tier available (512MB RAM, spins down after inactivity)

### Heroku

1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Login and create app:
```bash
heroku login
heroku create your-app-name
```
3. Set environment variables:
```bash
heroku config:set GROQ_API_KEY=your_key
heroku config:set TAVILY_API_KEY=your_key
heroku config:set HF_TOKEN=your_token
```
4. Deploy:
```bash
git push heroku main
```

**Cost**: Eco dynos ($5/month), includes free hours

### Docker

Build and run locally or on any container platform:

```bash
docker-compose up --build
# OR
docker build -t jansahayak .
docker run -p 5000:5000 --env-file .env jansahayak
```

**Platforms**: AWS ECS, Google Cloud Run, Azure Container Instances, DigitalOcean App Platform

### Vercel (Limited Support)

⚠️ **Note**: Vercel has significant limitations for ML applications:
- 50MB size limit (this app is ~200MB with dependencies)
- 10-second timeout (agent workflows can take 20-30s)
- Not recommended for production

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide with troubleshooting, security best practices, and platform comparisons.

## 📁 Project Structure

See code comments for detailed module documentation.

## 🎯 CPU-Only Deployment

This system runs entirely on CPU using:
- HuggingFace sentence-transformers for embeddings
- PyTorch CPU version
- FAISS CPU for vector search
- Groq API for LLM inference (no local GPU needed)
