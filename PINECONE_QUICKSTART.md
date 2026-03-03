# 🚀 Quick Start - Pinecone Integration

This guide will help you deploy JanSahayak with Pinecone on Render in **under 10 minutes**!

## Why This Setup?

✅ **Render Free Tier**: 512MB RAM  
✅ **Pinecone**: No memory usage on your server  
✅ **Result**: Your app fits perfectly! 🎉

---

## Step 1: Create Pinecone Account (2 minutes)

1. Go to [pinecone.io](https://www.pinecone.io/)
2. Click **"Sign Up"** (Free forever - no credit card!)
3. Verify your email and login

---

## Step 2: Get Pinecone API Key (1 minute)

1. In Pinecone dashboard, click **"API Keys"**
2. Copy your API key (starts with `pcsk_...`)
3. Keep this tab open!

---

## Step 3: Create Pinecone Index (2 minutes)

### Option A: Via Console (Easiest)

1. Click **"Create Index"** button
2. Fill in:
   ```
   Index Name: jansahayak-schemes
   Dimensions: 384
   Metric: cosine
   Plan: Starter (Free)
   ```
3. Click **"Create"** and wait 1 minute

### Option B: Via Python (After installing dependencies)

```bash
python init_embeddings.py --pinecone
# Will auto-create index if it doesn't exist
```

---

## Step 4: Update Local Environment (1 minute)

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` and add your keys:

```env
GROQ_API_KEY="your_groq_key"
TAVILY_API_KEY="your_tavily_key"
HF_TOKEN="your_hf_token"

# Add these new lines:
PINECONE_API_KEY="pcsk_your_actual_key_here"
PINECONE_INDEX_NAME="jansahayak-schemes"
VECTOR_STORE_MODE="pinecone"
```

---

## Step 5: Upload Documents to Pinecone (3 minutes)

**Run this LOCALLY** (one-time setup):

```bash
# Install dependencies first
pip install -r requirements.txt

# Upload your PDFs to Pinecone
python init_embeddings.py --pinecone
```

This will:
- ✅ Load PDFs from `data/schemes_pdfs/` and `data/exams_pdfs/`
- ✅ Generate embeddings
- ✅ Upload to Pinecone cloud
- ✅ No local storage needed!

**Expected output:**
```
📦 Downloading HuggingFace Embeddings Model
✅ Embeddings model downloaded and verified successfully!

☁️  Building Pinecone Vector Stores
📊 Processing Scheme Documents...
   Found X scheme PDF(s)
✅ Successfully uploaded X documents to Pinecone!
```

---

## Step 6: Configure Render Environment (2 minutes)

1. Go to your Render dashboard
2. Select your web service
3. Click **"Environment"** tab
4. Add these variables:

| Key | Value |
|-----|-------|
| `PINECONE_API_KEY` | `your_pinecone_api_key` |
| `PINECONE_INDEX_NAME` | `jansahayak-schemes` |
| `VECTOR_STORE_MODE` | `pinecone` |

5. Keep your existing keys (GROQ_API_KEY, etc.)

---

## Step 7: Deploy to Render! 

```bash
git add .
git commit -m "Add Pinecone integration"
git push
```

Render will automatically redeploy! 🚀

---

## ✅ Verification

Once deployed, check Render logs for:

```
📚 Initializing Vector Stores
☁️  Mode: Pinecone (Cloud Vector Database)
✅ Pinecone API Key: Found
✅ Index Name: jansahayak-schemes
✅ Pinecone scheme vectorstore connected
✅ Pinecone exam vectorstore connected
```

---

## 🎉 Success!

Your app is now running with:
- ✅ **Low Memory**: ~150MB (fits in Render free tier!)
- ✅ **Fast Queries**: Pinecone API
- ✅ **Scalable**: Add more PDFs anytime
- ✅ **No Storage**: All vectors in cloud

---

## 🔧 Managing Your Data

### Add More Documents

1. Add PDFs to `data/schemes_pdfs/` or `data/exams_pdfs/`
2. Run locally:
   ```bash
   python init_embeddings.py --pinecone
   ```
3. Documents automatically added to Pinecone!
4. No need to redeploy! ✨

### Check Pinecone Usage

Go to Pinecone dashboard → See your index stats:
- Number of vectors
- Storage used
- Queries per second

**Free tier includes:**
- 1 index ✅
- 100,000 vectors (you'll use ~1,000-5,000) ✅
- Unlimited queries ✅

---

## 🆘 Troubleshooting

### "Pinecone API key not found"
- Check `.env` file has `PINECONE_API_KEY`
- On Render: Verify environment variable is set correctly

### "Index not found"
- Make sure index name matches exactly: `jansahayak-schemes`
- Check index was created in Pinecone console

### "Dimension mismatch"
- Index must be 384 dimensions
- Delete index in Pinecone console and recreate

### "Out of memory on Render"
- Make sure `VECTOR_STORE_MODE=pinecone` is set
- Check you're not loading FAISS files

### App falls back to FAISS
- Pinecone credentials missing or invalid
- App will auto-fallback to FAISS (if available)
- Check logs for specific error

---

## 💰 Cost Analysis

| Service | Plan | Cost | What You Get |
|---------|------|------|--------------|
| **Render** | Free | $0 | 512MB RAM, 1 instance |
| **Pinecone** | Starter | $0 | 100K vectors, unlimited queries |
| **Groq** | Free | $0 | Fast LLM inference |
| **Tavily** | Free | $0 | 1000 searches/month |
| **Total** | | **$0** | Full production-ready app! 🎉 |

---

## 🔄 Local Development

Want to test locally without Pinecone?

```env
# In .env
VECTOR_STORE_MODE="faiss"
```

Then build local indexes:
```bash
python init_embeddings.py --faiss
```

This uses FAISS (local files) instead of Pinecone.

---

## 📞 Need Help?

1. Check [PINECONE_SETUP.md](PINECONE_SETUP.md) for detailed guide
2. Review [RENDER_TROUBLESHOOTING.md](RENDER_TROUBLESHOOTING.md)
3. Check Render logs for error messages
4. Verify all environment variables are set

---

## 🎓 What's Next?

- [ ] Add more scheme PDFs to improve recommendations
- [ ] Add exam PDFs for better exam suggestions
- [ ] Monitor Pinecone usage in dashboard
- [ ] Scale up Render plan if needed (after testing)

**You're all set! Happy deploying! 🚀**
