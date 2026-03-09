# 🚀 Quick Start: Deploy Agricultural Yield Prediction to Vercel

## ⚡ 5-Minute Setup

### 1. Prepare Your Local Environment

```bash
# Navigate to your project
cd agriculture_yield

# Copy environment template
copy .env.example .env

# Edit .env with your actual values
# GEMINI_API_KEY=your_key_here
# DB_HOST=your_host_here (etc.)
```

### 2. Test Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run local server
python api/index.py

# Visit: http://localhost:3000
```

### 3. Push to GitHub

```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### 4. Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

### 5. Add Environment Variables

In Vercel Dashboard:
1. Go to Project Settings → Environment Variables
2. Add each variable from your `.env` file
3. Trigger redeploy automatically or run: `vercel --prod`

## 📊 Final Project Structure

```
agriculture_yield/
├── api/
│   └── index.py                      ← Serverless function
├── public/                           ← Static files served directly
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   ├── index.html
│   ├── prediction.html
│   ├── history.html
│   └── error.html
├── models/
│   ├── random_forest_model.pkl
│   └── scaler.pkl
├── vercel.json                       ← Vercel config (already created)
├── requirements.txt                  ← Updated for Vercel
├── .gitignore                        ← Git ignore rules
├── .env.example                      ← Template for env vars
├── .env                              ← Your secret vars (NOT COMMITTED)
└── VERCEL_DEPLOYMENT_GUIDE.md        ← Full deployment guide
```

## 🔑 Required Environment Variables

Set these in Vercel dashboard:

```
GEMINI_API_KEY              → Your Google Gemini API key
DB_HOST                     → Your database host
DB_USER                     → Database username
DB_PASSWORD                 → Database password
DB_NAME                     → Database name
DB_PORT                     → Database port (usually 5432 for PostgreSQL)
```

## ✅ Verification Checklist

After deployment, verify:

- [ ] Home page loads: `https://your-app.vercel.app/`
- [ ] Health check: `https://your-app.vercel.app/health`
- [ ] Prediction form works
- [ ] Chat AI responds (if Gemini key configured)
- [ ] Check Vercel logs for errors: `vercel logs`

## 🐛 Common Issues & Fixes

| Problem | Solution |
|---------|----------|
| "Module not found" | Update requirements.txt: `pip freeze > requirements.txt` |
| DB connection fails | Check environment variables in Vercel dashboard |
| Templates not found | Ensure `api/index.py` has correct template_folder path |
| Timeout errors | Model files too large? Check Vercel function size limits |
| API key not working | Verify GEMINI_API_KEY is set in Vercel environment variables |

## 📖 Full Documentation

For detailed instructions, see: [VERCEL_DEPLOYMENT_GUIDE.md](VERCEL_DEPLOYMENT_GUIDE.md)

## 🌐 Accessing Your App

After successful deployment:

```
Home:               https://your-app-name.vercel.app/
Health Check:       https://your-app-name.vercel.app/health
Predict (POST):     https://your-app-name.vercel.app/predict
Chat API (POST/GET): https://your-app-name.vercel.app/chat
```

## 🎯 What Changed from Local XAMPP?

| Aspect | XAMPP (Local) | Vercel |
|--------|---------------|--------|
| **Server** | Apache/PHP | Serverless Python Functions |
| **Database** | localhost MySQL | Cloud Database (Supabase/AWS/etc) |
| **Entry Point** | app.py | api/index.py |
| **Config** | No config files | vercel.json |
| **Environment Variables** | .env with dotenv | Vercel dashboard secrets |
| **Static Files** | /public folder | public/ directory |
| **Cold Start** | None | First request slower (~1-2s) |
| **Scaling** | Manual | Automatic |

## 🚀 Next: Custom Domain Setup

After deployment works:

1. Buy domain (Namecheap, GoDaddy, Route53, etc.)
2. In Vercel Dashboard → Project Settings → Domains
3. Add your custom domain
4. Follow DNS configuration steps
5. HTTPS automatically enabled!

---

**🎉 Your app is ready for the cloud!**

Need help? → See VERCEL_DEPLOYMENT_GUIDE.md for full documentation
