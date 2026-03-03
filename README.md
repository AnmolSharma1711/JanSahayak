# 🙏 JanSahayak - AI-Powered Government Schemes & Exams Assistant

> Your personal AI assistant for discovering government schemes and competitive exam opportunities in India

[![Hugging Face Spaces](https://img.shields.io/badge/🤗-Hugging%20Face-yellow)](https://huggingface.co/spaces)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green)](https://flask.palletsprojects.com/)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-blue)](https://www.langchain.com/)

---

## 🌟 Features

### 🤖 Multi-Agent AI System
- **Profiling Agent**: Extracts structured user information
- **Scheme Agent**: Recommends relevant government schemes  
- **Exam Agent**: Suggests competitive exams based on qualifications
- **RAG Agent**: Retrieves information from curated document database

### 💡 Intelligent Capabilities
- ✅ Natural language understanding of user profiles
- ✅ Smart recommendations based on eligibility criteria
- ✅ RAG (Retrieval-Augmented Generation) with FAISS vectorstore
- ✅ Real-time web search via Tavily API
- ✅ PDF generation for saving recommendations
- ✅ Beautiful web interface with modern UI

---

## 🚀 Deploy to Hugging Face Spaces (Recommended)

### Why Hugging Face Spaces?
- ✅ **16GB RAM for FREE** (perfect for RAG apps!)
- ✅ Built for ML/AI applications
- ✅ Easy Git-based deployment
- ✅ Public URL instantly
- ✅ Auto-rebuild on push

### Quick Deploy Steps:

1. **Create Space** on [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Name: `jansahayak`
   - SDK: Select "Docker" or "Gradio"
   - Hardware: CPU basic (Free)

2. **Connect GitHub Repository**
   - Settings → Link to GitHub
   - Select this repository
   - Enable auto-sync

3. **Add Secrets** (Settings → Variables)
   ```
   GROQ_API_KEY=your_groq_key
   TAVILY_API_KEY=your_tavily_key  
   HF_TOKEN=your_hf_token (optional)
   SKIP_VECTORSTORES=false
   ```

4. **Push & Deploy!**
   ```bash
   git push origin main
   ```

Your app will be live at: `https://huggingface.co/spaces/YOUR_USERNAME/jansahayak`

---

## 🛠️ Local Development

```bash
# Clone and setup
git clone https://github.com/YOUR_USERNAME/JanSahayak.git
cd JanSahayak

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your keys

# Build vectorstores (optional - if you have PDFs)
python init_embeddings.py

# Run app
python app.py
# or use launcher scripts: start_web.bat (Windows) / ./start_web.sh (Linux/Mac)
```

Visit `http://localhost:5000`

---

## 🔑 Get API Keys

| Service | URL | Free Tier | Used For |
|---------|-----|-----------|----------|
| **Groq** | [console.groq.com](https://console.groq.com) | ✅ Yes | LLM Inference |
| **Tavily** | [tavily.com](https://tavily.com) | 1000 searches/mo | Web Search |
| **HuggingFace** | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) | ✅ Yes | Model Downloads |

---

## 💾 Adding Custom Documents

### Government Schemes PDFs
1. Place PDFs in `data/schemes_pdfs/`
2. Run `python init_embeddings.py`
3. Restart app

### Exam Information PDFs
1. Place PDFs in `data/exams_pdfs/`
2. Run `python init_embeddings.py`
3. Restart app

Automatically indexed and searchable via RAG!

---

## 🧪 Technology Stack

- **Backend**: Flask
- **AI**: LangChain + LangGraph  
- **LLM**: Groq (Llama 3.3 70B)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Vector DB**: FAISS (local)
- **Search**: Tavily API
- **Frontend**: HTML5 + CSS3 + JavaScript

---

## 📁 Project Structure

```
JanSahayak/
├── app.py                    # Flask web app
├── main.py                   # CLI interface
├── agents/                   # AI agents
│   ├── profiling_agent.py
│   ├── scheme_agent.py
│   ├── exam_agent.py
│   └── rag_agent.py
├── rag/                      # RAG components
│   ├── embeddings.py
│   ├── scheme_vectorstore.py
│   └── exam_vectorstore.py
├── data/                     # Documents
│   ├── schemes_pdfs/
│   └── exams_pdfs/
├── templates/                # HTML templates
└── static/                   # CSS/JS
```

---

## 🐛 Troubleshooting

**Memory issues on local machine?**
```env
# Set in .env
SKIP_VECTORSTORES=true
```
Uses web search only (no embeddings needed)

**Vectorstore errors?**
```bash
rm -rf rag/scheme_index rag/exam_index
python init_embeddings.py
```

---

## 🤝 Contributing

Contributions welcome! Fork → Create branch → Submit PR

---

## 📜 License

MIT License

---

## 🙏 Acknowledgments

Built with [LangChain](https://www.langchain.com/), [Groq](https://groq.com/), [Tavily](https://tavily.com/), and ❤️

---

Made for the people of India 🇮🇳
