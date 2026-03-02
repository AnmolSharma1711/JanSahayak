# 📚 JanSahayak - Usage Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [System Architecture](#system-architecture)
3. [Agent Details](#agent-details)
4. [Running the System](#running-the-system)
5. [API Keys Setup](#api-keys-setup)
6. [Adding Data](#adding-data)
7. [Advanced Usage](#advanced-usage)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start

### 1. Install Dependencies

```bash
# Activate virtual environment (if not already activated)
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install packages
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
# Copy example env file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Edit .env and add your API keys
```

**Required API Keys:**
- **GROQ_API_KEY**: Get from https://console.groq.com/
- **TAVILY_API_KEY**: Get from https://tavily.com/
- **HF_TOKEN** (optional): Get from https://huggingface.co/settings/tokens

### 3. Add PDF Data

```bash
# Add government scheme PDFs to:
data/schemes_pdfs/

# Add competitive exam PDFs to:
data/exams_pdfs/
```

### 4. Run Setup

```bash
python setup.py
```

This will:
- Check all dependencies
- Verify API keys
- Check PDF data
- Build vectorstores

### 5. Run the System

```bash
python main.py
```

---

## System Architecture

```
┌─────────────────┐
│   User Input    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Profiling Agent │ ──► Extracts structured profile
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌─────────┐
│Scheme  │ │  Exam   │
│Agent   │ │ Agent   │
└───┬────┘ └────┬────┘
    │           │
    ▼           │
┌────────────┐  │
│  Benefit   │  │
│  Agent     │  │
└─────┬──────┘  │
      │         │
      └────┬────┘
           ▼
    ┌─────────────┐
    │Final Output │
    └─────────────┘
```

---

## Agent Details

### 🧾 User Profiling Agent
**File:** `agents/profiling_agent.py`

**What it does:**
- Extracts structured information from user input
- Identifies: age, income, caste, education, state, interests, etc.
- Outputs JSON profile for other agents

**Input:** Raw user text
**Output:** Structured JSON profile

### 🏛️ Scheme Recommendation Agent
**File:** `agents/scheme_agent.py`

**What it does:**
- Uses RAG to search scheme database
- Optionally uses Tavily for live government website search
- Matches user profile with eligibility criteria
- Recommends suitable government schemes

**Input:** User profile
**Output:** Scheme recommendations with eligibility, benefits, application steps

### 🎓 Exam Recommendation Agent
**File:** `agents/exam_agent.py`

**What it does:**
- Searches exam database using RAG
- Matches based on education, age, interests
- Recommends competitive exams
- Provides exam details, preparation strategy, career scope

**Input:** User profile
**Output:** Exam recommendations with eligibility, dates, resources

### 🔎 Web Search Agent
**File:** `agents/search_agent.py`

**What it does:**
- Uses Tavily API for real-time search
- Focuses on .gov.in government domains
- Fetches latest scheme/exam information

**Input:** Search query
**Output:** Live search results from government websites

### 📚 RAG Retrieval Agent
**File:** `agents/rag_agent.py`

**What it does:**
- Performs semantic search on vectorstores
- Retrieves relevant scheme/exam documents
- Supports both scheme and exam databases

**Input:** Query string
**Output:** Relevant document chunks

### 📂 Document Processing Agent
**File:** `agents/document_agent.py`

**What it does:**
- Extracts text from PDF files
- Performs OCR on images
- Processes resumes and documents

**Input:** File path
**Output:** Extracted text

### 💰 Missed Benefits Calculator Agent
**File:** `agents/benefit_agent.py`

**What it does:**
- Calculates potential benefits user missed
- Estimates monetary and non-monetary losses
- Provides year-wise breakdown
- Suggests retroactive claims

**Input:** User profile + Scheme recommendations
**Output:** Missed benefits analysis with action items

---

## Running the System

### Interactive Mode

```bash
python main.py
```

Follow the prompts and enter your details. Example input:

```
I am a 25-year-old male from Maharashtra. I completed my Bachelor's in 
Engineering with 70% marks. My family income is around 3 lakh per year. 
I belong to the OBC category. I am currently unemployed and looking for 
government job opportunities. I am interested in technical positions 
and banking sector jobs.

Type 'done' or press Enter on empty line when finished.
```

### File Mode

Create a text file with user details:

```bash
# user_input.txt
I am a 25-year-old male from Maharashtra...
```

Run with file:

```bash
python main.py user_input.txt
```

### Output

Results are saved to `outputs/results_YYYYMMDD_HHMMSS.json`

The output includes:
- User profile (extracted)
- Scheme recommendations
- Exam recommendations
- Missed benefits analysis
- Any errors encountered

---

## API Keys Setup

### Groq API (Required)

1. Go to https://console.groq.com/
2. Sign up / Log in
3. Create a new API key
4. Copy to `.env` file as `GROQ_API_KEY`

**Why needed:** Powers the LLM brain of all agents

### Tavily API (Required for web search)

1. Go to https://tavily.com/
2. Sign up / Log in
3. Get your API key
4. Copy to `.env` file as `TAVILY_API_KEY`

**Why needed:** Enables live government website search

### HuggingFace Token (Optional)

1. Go to https://huggingface.co/settings/tokens
2. Create a new token
3. Copy to `.env` file as `HF_TOKEN`

**Why needed:** May help with downloading embedding models

---

## Adding Data

### Government Scheme PDFs

Add PDFs to: `data/schemes_pdfs/`

**Recommended sources:**
- https://www.india.gov.in/
- https://www.myscheme.gov.in/
- State government portals
- Ministry websites (.gov.in)

**Types of schemes to add:**
- PM Kisan Samman Nidhi
- Ayushman Bharat
- PM Awas Yojana
- Scholarships (SC/ST/OBC/Minority)
- Skill Development Programs
- State-specific schemes

### Competitive Exam PDFs

Add PDFs to: `data/exams_pdfs/`

**Recommended sources:**
- UPSC: https://upsc.gov.in/
- SSC: https://ssc.nic.in/
- IBPS: https://ibps.in/
- RRB: https://rrbapply.gov.in/
- State PSCs

**Types of exams to add:**
- Official notifications
- Syllabus documents
- Exam patterns
- Previous year papers info
- Eligibility criteria documents

### Building Vectorstores

After adding PDFs, build vectorstores:

```bash
python setup.py --build-vectorstores
```

Or in Python:

```python
from rag.scheme_vectorstore import build_scheme_vectorstore
from rag.exam_vectorstore import build_exam_vectorstore

build_scheme_vectorstore()
build_exam_vectorstore()
```

---

## Advanced Usage

### Running Individual Agents

#### Test Profiling Agent

```python
from agents.profiling_agent import run_profiling_agent

user_input = "I am 25 years old from Maharashtra, OBC category..."
profile = run_profiling_agent(user_input)
print(profile)
```

#### Test Scheme Agent

```python
from agents.scheme_agent import run_scheme_agent

profile = {
    "age": 25,
    "income": "300000",
    "caste": "OBC",
    "state": "Maharashtra"
}

result = run_scheme_agent(profile, use_web_search=False)
print(result)
```

#### Test Exam Agent

```python
from agents.exam_agent import run_exam_agent

profile = {
    "education": "Bachelor's in Engineering",
    "age": 25,
    "interests": "Technical jobs"
}

result = run_exam_agent(profile)
print(result)
```

### Using Agent I/O Handlers

```python
from agent_io.scheme_io import SchemeIO

io = SchemeIO()

# Write input
io.write_input(profile_data, preferences={"priority": "high_benefit"})

# Write output
io.write_output(recommendations, metadata={"sources": 5})

# Read output
previous_results = io.read_output()
```

### Custom Workflow

```python
from graph.workflow import build_workflow

app = build_workflow()

state = {
    "user_input": "Your text here...",
    "errors": []
}

result = app.invoke(state)
print(result["final_output"])
```

---

## Troubleshooting

### Error: "GROQ_API_KEY not found"

**Solution:** 
- Check `.env` file exists
- Verify API key is added correctly
- No spaces around `=` sign: `GROQ_API_KEY=your_key_here`

### Error: "Vectorstore not found"

**Solution:**
```bash
python setup.py --build-vectorstores
```

### Error: "No PDF files found"

**Solution:**
- Add PDF files to `data/schemes_pdfs/` or `data/exams_pdfs/`
- Ensure files have `.pdf` extension

### Import Errors

**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Slow Performance

**Tips:**
- Vectorstore building is one-time (will be slow first time)
- Groq API should be fast (<1s per call)
- If web search is slow, disable with `use_web_search=False`

### OCR Not Working (pytesseract)

**Solution (Windows):**
1. Download Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
2. Install Tesseract
3. Add to PATH or set in code:
   ```python
   import pytesseract
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

---

## Best Practices

1. **Keep PDFs Updated**: Regularly update scheme and exam PDFs
2. **Rebuild Vectorstores**: After adding new PDFs, rebuild vectorstores
3. **Test Each Agent**: Test individual agents before running full workflow
4. **Monitor API Usage**: Track Groq and Tavily API usage
5. **Save Outputs**: All results are automatically saved to `outputs/`

---

## Support

For issues or questions:
1. Check this guide first
2. Review error messages
3. Test individual components
4. Check PDF data quality
5. Verify API keys

---

## System Requirements

- **Python**: 3.8+
- **RAM**: 4GB minimum (8GB recommended for embedding models)
- **Storage**: 2GB for dependencies + storage for PDFs
- **Internet**: Required for Groq and Tavily APIs
- **OS**: Windows, Linux, or macOS

---

## Performance Notes

- **CPU-Only**: System runs entirely on CPU
- **First Run**: Slower due to model downloads
- **Subsequent Runs**: Fast with cached models
- **Vectorstore Building**: One-time process, can take time depending on PDF count
- **Query Time**: ~2-5 seconds per agent (with Groq API)

---

## Development

To contribute or modify:

1. Each agent is independent (in `agents/`)
2. Prompts are separated (in `prompts/`)
3. Workflow is in `graph/workflow.py`
4. Add new agents by creating new node functions
5. Modify prompts to fine-tune agent behavior

---

**Happy Analyzing! 🚀**
