# Pinecone Integration Guide for JanSahayak

## Why Pinecone?
- **Free Tier**: 1 index with 100K vectors (plenty for your use case)
- **Serverless**: No memory usage on your Render instance
- **Fast**: Better performance than local FAISS
- **Scalable**: Easy to add more documents later

---

## Step 1: Create Pinecone Account

1. Go to [https://www.pinecone.io/](https://www.pinecone.io/)
2. Click "Sign Up" (Free forever plan)
3. Verify your email
4. Login to Pinecone console

---

## Step 2: Get API Key

1. In Pinecone console, go to **API Keys** section
2. Copy your API key (starts with `pcsk_...` or similar)
3. Note your environment (usually `us-east-1` for free tier)

---

## Step 3: Create Index

### Option A: Via Pinecone Console (Recommended for first time)

1. Click **"Create Index"** button
2. Fill in details:
   - **Index Name**: `jansahayak-schemes`
   - **Dimensions**: `384` (for all-MiniLM-L6-v2 model)
   - **Metric**: `cosine`
   - **Cloud & Region**: Choose default (usually AWS us-east-1)
   - **Plan**: Starter (Free)
3. Click **"Create Index"**
4. Wait 1-2 minutes for index to be ready

### Option B: Via Python (After installing pinecone-client)

```python
from pinecone import Pinecone

pc = Pinecone(api_key="your-api-key")
pc.create_index(
    name="jansahayak-schemes",
    dimension=384,
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1")
)
```

---

## Step 4: Update Environment Variables

Add to your `.env` file:

```env
# Existing keys
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
HF_TOKEN=your_hf_token

# New Pinecone keys
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=jansahayak-schemes
```

**For Render.com:**
1. Go to your Render dashboard
2. Select your web service
3. Go to **Environment** tab
4. Add these environment variables:
   - `PINECONE_API_KEY`: Your Pinecone API key
   - `PINECONE_INDEX_NAME`: `jansahayak-schemes`

---

## Step 5: Install Dependencies

Run locally:
```bash
pip install pinecone-client langchain-pinecone
```

I've already updated `requirements.txt` for you.

---

## Step 6: Upload Your Documents to Pinecone

Run this **locally** (one-time setup):

```bash
python init_embeddings.py --pinecone
```

This will:
1. Load PDFs from `data/schemes_pdfs/`
2. Generate embeddings
3. Upload to Pinecone (no local storage needed!)

---

## Step 7: Deploy to Render

Now when you deploy to Render:
- ✅ No FAISS files needed
- ✅ No model loading on server (embeddings on-demand)
- ✅ Low memory usage (<200MB)
- ✅ Fast queries via Pinecone API

Just commit and push:
```bash
git add .
git commit -m "Integrate Pinecone for vector storage"
git push
```

Render will automatically redeploy!

---

## Benefits

### Before (FAISS):
- 📦 Had to load entire index into RAM (~80MB)
- 🧠 Model loaded in memory (~200MB)
- ❌ Total: >500MB = Out of Memory on Render

### After (Pinecone):
- ☁️ Vectors stored in cloud
- 🔍 Query via API (minimal memory)
- ✅ Total: ~150MB = Fits in Render free tier!

---

## Troubleshooting

### "Index not found"
- Make sure index name matches exactly in `.env`
- Check index is created in Pinecone console

### "API key invalid"
- Verify API key is correct in `.env`
- Check no extra spaces in the key

### "Dimension mismatch"
- Index must be 384 dimensions for all-MiniLM-L6-v2
- Delete and recreate index if dimension is wrong

---

## Cost Estimate

Pinecone Free Tier:
- ✅ 1 index (you need 1)
- ✅ 100,000 vectors (you'll use ~1,000-5,000)
- ✅ Unlimited queries
- ✅ No credit card required

**You're well within limits!** 🎉

---

## Next Steps

1. ✅ Create Pinecone account
2. ✅ Get API key
3. ✅ Create index (dimension=384)
4. ✅ Update `.env` with credentials
5. ✅ Run `python init_embeddings.py --pinecone` locally
6. ✅ Deploy to Render

Need help? Check the updated code files I've created!
