# 🚀 JanSahayak Quick Start Card

## Installation (One-Time Setup)

```bash
# 1. Activate virtual environment
.venv\Scripts\activate         # Windows
source .venv/bin/activate      # Linux/Mac

# 2. Install dependencies (if not done)
pip install -r requirements.txt

# 3. Setup API keys in .env file
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key

# 4. Add PDFs to data folders (optional)
data/schemes_pdfs/    # Government schemes
data/exams_pdfs/      # Competitive exams

# 5. Build vectorstores (if PDFs added)
python setup.py --build-vectorstores
```

## Running the Application

### 🌐 Web Interface (Recommended)

**Option 1: Using Python**
```bash
python app.py
```

**Option 2: Using Batch File (Windows)**
```bash
start_web.bat
```

**Option 3: Using Shell Script (Linux/Mac)**
```bash
./start_web.sh
```

Then open: **http://localhost:5000**

### 💻 Command Line Interface

```bash
python main.py
```

## Web UI Features

| Page | URL | Purpose |
|------|-----|---------|
| **Home** | `/` | Input form with examples |
| **Results** | `/result/<id>` | View analysis results |
| **About** | `/about` | System information |
| **History** | `/history` | Past analyses |

## Quick Examples

### Student Profile
```
I am a 22-year-old female student from Karnataka. My family's 
annual income is around 2.5 lakh rupees. I belong to the SC 
category. I am currently pursuing my Bachelor's degree in 
Computer Science. I am interested in government IT sector jobs.
```

### Farmer Profile
```
I am a 45-year-old male farmer from Madhya Pradesh. My family's 
annual income is around 1.5 lakh rupees from agriculture. I 
belong to the OBC category. I own 3 acres of land. Looking for 
farming subsidies and crop insurance schemes.
```

### Job Seeker Profile
```
I am a 28-year-old male from Uttar Pradesh. My family's annual 
income is around 4 lakh rupees. I belong to the General category. 
I completed my MBA 2 years ago. Currently unemployed and seeking 
government jobs in banking, railways, or state PSC positions.
```

## Common Commands

```bash
# Check system setup
python setup.py --check

# Build vectorstores
python setup.py --build-vectorstores

# Start web server
python app.py

# Run CLI version
python main.py

# Test individual agent
python -m agents.profiling_agent
python -m agents.scheme_agent
python -m agents.exam_agent
```

## File Locations

| Item | Location |
|------|----------|
| **Results** | `outputs/results_*.json` |
| **Scheme PDFs** | `data/schemes_pdfs/` |
| **Exam PDFs** | `data/exams_pdfs/` |
| **Vectorstores** | `rag/scheme_index/`, `rag/exam_index/` |
| **Config** | `.env` |
| **Templates** | `templates/` |
| **Static Files** | `static/css/`, `static/js/` |

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Tab` | Navigate form fields |
| `Ctrl+Enter` | Submit form |
| `Esc` | Close modals |

## Troubleshooting

### Error: Module not found
```bash
pip install -r requirements.txt --upgrade
```

### Error: Vectorstore not found
```bash
python setup.py --build-vectorstores
```

### Error: API key not found
Check `.env` file has correct keys without spaces:
```
GROQ_API_KEY=gsk_xxxxx
TAVILY_API_KEY=tvly_xxxxx
```

### Port 5000 already in use
Change port in `app.py`:
```python
app.run(debug=True, port=8080)
```

### Slow analysis
- Ensure vectorstores are built
- Check internet connection
- Verify API keys are valid

## API Keys

### Groq API
- **Get from:** https://console.groq.com/
- **Purpose:** LLM inference
- **Free tier:** Available

### Tavily API
- **Get from:** https://tavily.com/
- **Purpose:** Web search
- **Free tier:** Available

## System Requirements

- ✅ Python 3.8+
- ✅ 4GB RAM (8GB recommended)
- ✅ 2GB storage
- ✅ Internet connection
- ✅ Modern web browser

## Quick Links

- 📖 Full Documentation: `README.md`
- 🌐 Web UI Guide: `WEB_UI_GUIDE.md`
- 📚 Usage Guide: `USAGE_GUIDE.md`
- 🏗️ Architecture: `ARCHITECTURE.txt`
- 🎨 UI Preview: `UI_PREVIEW.md`

## Support

1. Check documentation first
2. Run `python setup.py --check`
3. Verify `.env` configuration
4. Ensure PDFs are in correct folders
5. Rebuild vectorstores if needed

---

**Happy Analyzing! 🎉**

**Start with:** `python app.py` → **http://localhost:5000**
