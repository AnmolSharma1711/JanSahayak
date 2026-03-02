# Render Deployment Troubleshooting Guide

## Common Issue: "Failed to execute 'json' on 'Response': Unexpected end of JSON input"

This error occurs when the server returns an HTML error page instead of JSON, usually due to:

### 1. **Missing API Keys** (Most Common)
The application requires these environment variables to be set on Render:

- `GROQ_API_KEY` - **Required** - For LLM operations
- `TAVILY_API_KEY` - **Required** - For web search functionality  
- `HF_TOKEN` - Optional - For HuggingFace embeddings

#### How to Fix:
1. Go to your Render dashboard
2. Select your `jansahayak` service
3. Go to **Environment** tab
4. Add the missing environment variables:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   HF_TOKEN=your_huggingface_token_here (optional)
   HF_HOME=/opt/render/.cache/huggingface
   ```
5. Click **Save Changes**
6. Render will automatically redeploy

---

## Vector Store & Embeddings Setup (RAG Functionality)

### What Happens During Deployment

The `render.yaml` buildCommand includes `python init_embeddings.py` which:

1. **Downloads HuggingFace Embeddings** (~80MB)
   - Model: `sentence-transformers/all-MiniLM-L6-v2`
   - Cached in `HF_HOME` directory for reuse
   
2. **Verifies Vector Stores**
   - Checks `rag/scheme_index/index.faiss` exists (✅ included in git)
   - Builds `rag/exam_index/` if exam PDFs are present

3. **Tests Embeddings**
   - Runs a test query to ensure everything works

### If Build Fails

Check Render build logs for:

```
❌ Failed to download embeddings: [error message]
```

**Common causes:**
- Build timeout (free tier has limits)
- Network issues downloading model
- Insufficient memory

**Solutions:**
1. **Increase timeout** - Render free tier may timeout on large downloads
2. **Check logs** - Look for specific error messages
3. **Retry deployment** - Sometimes temporary network issues

### Vector Store Files

These files MUST be in your git repository:

```
rag/
├── scheme_index/
│   ├── index.faiss  ← Binary vector index
│   └── index.pkl    ← Metadata pickle file
└── exam_index/      ← Optional (auto-built if PDFs present)
    ├── index.faiss
    └── index.pkl
```

**Check if files are tracked:**
```bash
git ls-files | grep "index\\.faiss"
```

### How RAG + Search Works

1. **Primary**: Vector store retrieval (fast, offline)
2. **Enhancement**: Tavily web search (live, current data)
3. **Fallback**: If vectorstore fails, uses web search only

---

## Request Timeout Issues

### 2. **Request Timeout**
Render's free tier has a 30-second timeout. The AI analysis might take longer.

#### How to Check:
- Visit `https://jansahayak-mthf.onrender.com/health` to check if API keys are configured
- Check Render logs for timeout errors

#### Solutions:
- Embeddings are pre-downloaded during build (not runtime)

### 3. **Memory Issues**
The free tier has limited memory. Vector stores and embeddings can be memory-intensive.

#### How to Fix:
- Consider upgrading to a paid plan
- Or optimize vector store loading (lazy loading)

### 4. **Build/Dependency Issues**
Missing dependencies or failed builds.

#### How to Check:
1. Go to Render dashboard → Logs
2. Look for build errors or missing packages
3. Check if all dependencies in `requirements.txt` are installing correctly

## Health Check Endpoint

The application now includes a health check endpoint:

```
GET /health
```

Returns:
```json
{
  "status": "ok",
  "service": "JanSahayak",
  "api_keys_configured": {
    "groq": true,
    "tavily": true,
    "hf_token": true
  }
}
```

## Improved Error Handling

The application now:
- ✅ Checks API keys before processing requests
- ✅ Returns proper JSON errors with clear messages
- ✅ Shows API key status on startup in logs
- ✅ Frontend handles non-JSON responses gracefully

## Checking Render Logs

1. Go to Render dashboard
2. Select your service
3. Click on **Logs** tab
4. Look for these messages on startup:
   ```
   ✅ GROQ_API_KEY is configured
   ✅ TAVILY_API_KEY is configured
   ⚠️  WARNING: HF_TOKEN is not set (optional but recommended)
   ```

## Testing Locally

Before deploying, test locally:

1. Create `.env` file with your API keys:
   ```
   GROQ_API_KEY=your_key_here
   TAVILY_API_KEY=your_key_here
   HF_TOKEN=your_token_here
   ```

2. Run the app:
   ```bash
   python app.py
   ```

3. Visit `http://localhost:5000/health` to verify configuration

## Next Steps

1. **Set environment variables on Render** (most likely fix)
2. Check Render logs for specific error messages
3. Visit `/health` endpoint to verify API keys are configured
4. Monitor the logs during a request to see exact error
5. If timeout issues persist, consider optimizing or upgrading plan

## Getting API Keys

- **Groq API**: https://console.groq.com/
- **Tavily API**: https://tavily.com/
- **HuggingFace Token**: https://huggingface.co/settings/tokens
