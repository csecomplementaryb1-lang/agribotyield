# 🌾 Agricultural Yield Prediction System - Vercel Deployment

Welcome! This project has been configured for deployment on **Vercel** serverless platform. Whether you want to deploy locally or on the cloud, this guide has you covered.

## 🎯 Quick Links

- **Want to deploy right now?** → [QUICK_START_VERCEL.md](QUICK_START_VERCEL.md) (5 minutes)
- **Need detailed instructions?** → [VERCEL_DEPLOYMENT_GUIDE.md](VERCEL_DEPLOYMENT_GUIDE.md)
- **Migrating from XAMPP?** → [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
- **Need CLI commands?** → [COMMAND_REFERENCE.md](COMMAND_REFERENCE.md)
- **Project structure?** → [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md)

## 📋 What's Included

### 🚀 Vercel Configuration
- ✅ `api/index.py` - Serverless entry point
- ✅ `vercel.json` - Vercel configuration
- ✅ `requirements.txt` - Vercel-compatible dependencies
- ✅ `.gitignore` - For secure deployment

### 📚 Documentation (4 comprehensive guides)
- ✅ Quick start guide (5 minutes)
- ✅ Full deployment guide (step-by-step)
- ✅ Migration guide (XAMPP to Vercel)
- ✅ Command reference (all CLI commands)

### 🛠️ Tools
- ✅ `setup_vercel.py` - Project verification script
- ✅ `.env.example` - Environment configuration template

## 🚀 Quick Start

### Option 1: Deploy to Vercel (Recommended)

```bash
# 1. Copy environment template
copy .env.example .env

# 2. Edit .env with your cloud database credentials
notepad .env

# 3. Test locally
python api/index.py

# 4. Push to GitHub
git push origin main

# 5. Deploy to Vercel
vercel --prod
```

**Time:** ~30 minutes (including database setup)

### Option 2: Run Locally

```bash
# 1. Setup environment
copy .env.example .env
# Edit .env with your database credentials

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run locally
python api/index.py

# 4. Visit http://localhost:3000
```

**Time:** ~5 minutes

## 💬 What Is This Project?

An **Agricultural Yield Prediction System** for Tamil Nadu, India:

- 🌾 **Predicts crop yields** based on:
  - District (region)
  - Crop type
  - Rainfall, temperature
  - Soil pH, nutrients (N, P, K)
  - Farm size

- 🤖 **AI Chat Assistant** (powered by Google Gemini):
  - Farm advice
  - Crop recommendations
  - Fertilizer guidance
  - Support in Tamil Nadu context

- 📊 **Prediction History**:
  - Stores past predictions
  - Shows trends over time

- 🔬 **Machine Learning**:
  - Random Forest model
  - Trained on agricultural data

## 🏗️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Flask (Python) |
| **Database** | Cloud (PostgreSQL/MongoDB) |
| **ML Model** | scikit-learn (Random Forest) |
| **AI Chat** | Google Gemini API |
| **Hosting** | Vercel Serverless |
| **Frontend** | HTML5, CSS3, JavaScript |

## 🔧 Key Features

### ✨ For Users
- 🌐 Web interface
- 📱 Responsive design
- 🤖 AI chatbot
- 📊 Prediction history
- 🔐 Secure deployment

### ⚙️ For Developers
- 🚀 One-click deployment
- 🔄 Auto-redeploy on GitHub push
- 📈 Automatic scaling
- 🌍 Global edge network
- 📝 Detailed documentation

## 📊 Project Structure

```
agriculture_yield/
├── api/index.py              ← Entry point for Vercel
├── templates/                ← HTML pages
├── public/                   ← CSS, JS, images
├── models/                   ← ML models
├── vercel.json              ← Vercel config
├── requirements.txt         ← Python packages
├── QUICK_START_VERCEL.md    ← 5-min guide
├── VERCEL_DEPLOYMENT_GUIDE.md  ← Full guide
└── ... (other docs)
```

## 🎯 Deployment Path

### Step 1: Local Setup
```bash
python api/index.py
# Test at http://localhost:3000
```

### Step 2: Push to GitHub
```bash
git push origin main
```

### Step 3: Deploy to Vercel
```bash
vercel --prod
# Your app lives at: your-app.vercel.app
```

### Step 4: Monitor
```bash
vercel logs your-app.vercel.app
```

## 🔐 Security

- ✅ Secrets in Vercel vault (not in code)
- ✅ HTTPS automatic
- ✅ Environment isolated
- ✅ No hardcoded credentials
- ✅ .env in .gitignore

## 📱 Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers

## 🌍 What Changed from XAMPP

| Aspect | XAMPP | Vercel |
|--------|-------|--------|
| Database | Localhost MySQL | Cloud (your choice) |
| Hosting | Your Machine | Vercel Edge Network |
| Deployment | Manual | Push to GitHub |
| HTTPS | Manual | Automatic |
| Scaling | Manual | Automatic |
| Entry Point | app.py | api/index.py |
| Cost | Free (electricity) | Free tier |

## 📖 Documentation

All guides are provided for different needs:

1. **In a hurry?** → [QUICK_START_VERCEL.md](QUICK_START_VERCEL.md)
2. **Need detailed steps?** → [VERCEL_DEPLOYMENT_GUIDE.md](VERCEL_DEPLOYMENT_GUIDE.md)
3. **Upgrading from XAMPP?** → [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
4. **Looking for commands?** → [COMMAND_REFERENCE.md](COMMAND_REFERENCE.md)
5. **Understanding changes?** → [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md)

## ✅ Pre-Deployment Checklist

Before deploying, ensure:

- [ ] Cloud database selected (Supabase, AWS, MongoDB, etc.)
- [ ] Database tables created
- [ ] `.env` file filled with credentials
- [ ] Local test successful (`python api/index.py`)
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Vercel account created
- [ ] Gemini API key obtained (optional but recommended)

## 🚀 Deployment Result

After successful deployment, you get:

✅ **Live URL:** `https://your-app.vercel.app`
✅ **Auto HTTPS:** Secure by default
✅ **Global CDN:** Fast everywhere
✅ **Auto Scaling:** Handles traffic spikes
✅ **CI/CD:** Auto-deploy on GitHub push
✅ **Monitoring:** Built-in analytics

## 🐛 Need Help?

### Common Issues

| Problem | Solution |
|---------|----------|
| 404 on routes | Check `vercel.json` routes |
| DB connection fails | Verify credentials in `.env` |
| Templates not found | Ensure template_folder path correct |
| Slow first load | Normal! Vercel cold start (~1-2s) |

### Documentation Order
1. Start with: [QUICK_START_VERCEL.md](QUICK_START_VERCEL.md)
2. If needed: [VERCEL_DEPLOYMENT_GUIDE.md](VERCEL_DEPLOYMENT_GUIDE.md)
3. For issues: [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) → Troubleshooting
4. For commands: [COMMAND_REFERENCE.md](COMMAND_REFERENCE.md)

## 📝 Example Deployment

```bash
# Step 1: Prepare environment
copy .env.example .env
# Edit .env:
# GEMINI_API_KEY=sk-...
# DB_HOST=your-db.supabase.co
# DB_USER=postgres
# DB_PASSWORD=...
# DB_NAME=postgres
# DB_PORT=5432

# Step 2: Test locally
python api/index.py
# ✅ Visit http://localhost:3000

# Step 3: Push to GitHub
git add .
git commit -m "Ready for Vercel"
git push origin main

# Step 4: Deploy to Vercel
npm install -g vercel
vercel --prod

# Step 5: Set environment variables in Vercel dashboard
# (Copy all from .env)

# Step 6: Monitor
vercel logs your-app.vercel.app

# ✅ Done! Visit https://your-app.vercel.app
```

## 🔑 Required API Keys

### Essential
- **Gemini API Key** (for chat)
  - Get from: https://aistudio.google.com/
  - Free tier available

### Database Credentials
- Choose ONE:
  - PostgreSQL (Supabase, AWS, GCP)
  - MongoDB (MongoDB Atlas)
  - Firebase (Google Cloud)

## 💰 Cost Estimate

| Service | Free Tier | Notes |
|---------|-----------|-------|
| Vercel | 100GB bandwidth | Perfect for MVP |
| Supabase PostgreSQL | 500MB | Free for small projects |
| MongoDB Atlas | 512MB | Free for hobby projects |
| Google Gemini | Limited calls | Free tier available |

## 🎯 Next Steps

1. **Right now:** Read [QUICK_START_VERCEL.md](QUICK_START_VERCEL.md) (5 min)
2. **Today:** Set up cloud database
3. **Today:** Deploy to Vercel
4. **This week:** Configure custom domain
5. **This week:** Monitor and optimize

## 📞 Support Resources

- **Vercel Docs:** https://vercel.com/docs
- **Flask Docs:** https://flask.palletsprojects.com/
- **Supabase:** https://supabase.com/docs
- **Google Gemini:** https://ai.google.dev/
- **MongoDB:** https://docs.mongodb.com/

## 🎉 Ready?

Pick your starting point:

- **Impatient:** [QUICK_START_VERCEL.md](QUICK_START_VERCEL.md)
- **Thorough:** [VERCEL_DEPLOYMENT_GUIDE.md](VERCEL_DEPLOYMENT_GUIDE.md)
- **Migrating:** [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
- **Commands:** [COMMAND_REFERENCE.md](COMMAND_REFERENCE.md)

---

## Changes from Original

This project has been enhanced for Vercel deployment:

✅ Added `api/index.py` (serverless entry point)
✅ Created `vercel.json` (configuration)
✅ Updated `requirements.txt` (Vercel compatible)
✅ Added `.gitignore` (secure secrets)
✅ Created 4 detailed guides
✅ Added `setup_vercel.py` (verification)

**Original functionality preserved** - all features work as before, just on the cloud!

---

**Built with:** Flask, scikit-learn, Google Gemini, Vercel
**For:** Tamil Nadu farmers & agricultural professionals
**Deployed on:** Vercel serverless platform

**Ready to deploy? → [QUICK_START_VERCEL.md](QUICK_START_VERCEL.md)** 🚀
