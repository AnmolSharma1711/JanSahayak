# Deployment Guide - JanSahayak

This guide covers deploying the JanSahayak Multi-Agent System to cloud platforms.

## 🚀 Quick Overview

**Recommended Platform**: Render or Heroku (both support full Flask apps with heavy dependencies)

**Why not Vercel?** Vercel is optimized for serverless/JAMstack. This app requires:
- Long-running Flask server
- Heavy ML dependencies (PyTorch, transformers, FAISS)
- Persistent vector databases
- Background processing

---

## 📦 Option 1: Deploy to Render (Recommended)

### Prerequisites
- GitHub account with your code
- Render account (https://render.com)
- API keys (Groq, Tavily, HuggingFace)

### Steps

1. **Push code to GitHub** (already done ✓)

2. **Go to Render Dashboard**
   - Visit https://dashboard.render.com
   - Click "New +" → "Web Service"

3. **Connect Repository**
   - Select your `JanSahayak` repository
   - Branch: `main`

4. **Configure Service**
   - Name: `jansahayak`
   - Region: Choose closest to you
   - Branch: `main`
   - Runtime: `Python 3`
   - Build Command: `pip install --upgrade pip && pip install -r requirements.txt`
   - Start Command: `python app.py`
   - Instance Type: Free (or paid for better performance)

5. **Set Environment Variables**
   - Go to "Environment" tab
   - Add these variables:
     ```
     GROQ_API_KEY=your_groq_key
     TAVILY_API_KEY=your_tavily_key
     HF_TOKEN=your_hf_token
     ```

6. **Deploy**
   - Click "Create Web Service"
   - Wait 10-15 minutes for build (large dependencies)
   - Your app will be live at: `https://jansahayak.onrender.com`

### Build Vectorstore (One-time)
After first deployment, SSH into your instance or use Render Shell:
```bash
python setup.py --build-vectorstores
```

---

## 📦 Option 2: Deploy to Heroku

### Prerequisites
- Heroku account (https://heroku.com)
- Heroku CLI installed
- API keys

### Steps

1. **Install Heroku CLI**
   ```bash
   # Windows
   choco install heroku-cli
   
   # Or download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create jansahayak-india
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set GROQ_API_KEY="your_groq_key"
   heroku config:set TAVILY_API_KEY="your_tavily_key"
   heroku config:set HF_TOKEN="your_hf_token"
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Open App**
   ```bash
   heroku open
   ```

### Upgrade Dynos (Optional)
Free tier has limited memory. For ML models:
```bash
heroku ps:scale web=1:standard-1x
```

---

## 📦 Option 3: Vercel (Limited - Serverless Only)

⚠️ **Warning**: Vercel has significant limitations for this app:
- 50MB deployment size limit (your dependencies exceed this)
- 10s function timeout on free tier
- No persistent file storage
- Not ideal for heavy ML workloads

### If you still want to try:

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel --prod
   ```

4. **Set Environment Variables**
   - Go to Vercel Dashboard → Project → Settings → Environment Variables
   - Add: `GROQ_API_KEY`, `TAVILY_API_KEY`, `HF_TOKEN`

**Note**: You'll likely hit size/timeout limits. Not recommended for this project.

---

## 🔧 Pre-Deployment Checklist

### 1. Update app.py for production
Change the last line from:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```
to:
```python
port = int(os.environ.get('PORT', 5000))
app.run(debug=False, host='0.0.0.0', port=port)
```

### 2. Optimize requirements.txt
For faster builds, pin versions:
```bash
pip freeze > requirements.txt
```

### 3. Pre-build vectorstores (Optional)
Build locally and commit:
```bash
python setup.py --build-vectorstores
git add rag/scheme_index/ rag/exam_index/
git commit -m "Add pre-built vectorstores"
git push
```

### 4. Add health check endpoint (Optional)
Add to app.py:
```python
@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200
```

---

## 🐳 Option 4: Docker Deployment

If you want to use Docker (works with Render, Railway, Fly.io):

1. **Create Dockerfile** (see separate file)
2. **Build**: `docker build -t jansahayak .`
3. **Run**: `docker run -p 5000:5000 --env-file .env jansahayak`

---

## 📊 Performance Considerations

### Memory Requirements
- Minimum: 512MB
- Recommended: 1GB+ (for ML models)
- PyTorch CPU + Transformers: ~500MB
- FAISS indexes: ~1-2MB per 1000 documents

### Build Time
- First deploy: 10-20 minutes (installing dependencies)
- Subsequent deploys: 2-5 minutes (cached)

### Cold Start
- Render/Heroku free tier: 30s-1min cold start
- Paid tier: Instant

---

## 🔐 Security Best Practices

1. **Never commit .env file** ✓ (already in .gitignore)
2. **Use environment variables** for API keys
3. **Enable HTTPS** (automatic on Render/Heroku)
4. **Regenerate exposed API keys**
5. **Set rate limiting** for production

---

## 🆘 Troubleshooting

### Build fails with "out of memory"
- Upgrade to paid tier with more RAM
- Or reduce dependencies (remove unused models)

### "Application Error" on startup
- Check logs: `heroku logs --tail` or Render logs
- Verify environment variables are set
- Ensure PORT is read from environment

### Vectorstore not found
- Build during deployment or commit pre-built indexes
- Check file permissions

### Slow response times
- Upgrade dyno/instance type
- Use persistent disk for caching
- Consider Redis for session storage

---

## 📝 Cost Estimates

### Free Tier
- **Render**: 750 hours/month, sleeps after inactivity
- **Heroku**: 1000 hours/month, sleeps after 30min
- **Vercel**: 100GB bandwidth (not suitable for this app)

### Paid Tiers
- **Render**: $7/month (Starter)
- **Heroku**: $7/month (Eco dyno)
- **Railway**: $5/month (Starter)

---

## ✅ Recommended Setup

For production deployment:

1. **Platform**: Render (easiest) or Heroku (more features)
2. **Plan**: Starter/Eco ($7/month) for consistent uptime
3. **Database**: None needed (stateless, uses APIs)
4. **Storage**: Commit vectorstores or rebuild on deploy
5. **Monitoring**: Use platform's built-in logs

---

## 🔗 Useful Links

- [Render Python Guide](https://render.com/docs/deploy-flask)
- [Heroku Python Guide](https://devcenter.heroku.com/articles/getting-started-with-python)
- [Flask Production Best Practices](https://flask.palletsprojects.com/en/latest/deploying/)

---

## 📞 Support

For deployment issues:
- Check platform-specific documentation
- Review application logs
- Verify all environment variables are set
- Test locally first with `python app.py`
