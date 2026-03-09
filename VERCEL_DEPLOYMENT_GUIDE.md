# 🚀 Vercel Deployment Guide - Agricultural Yield Prediction System

## Project Structure (Vercel-Compatible)

```
agriculture_yield/
├── api/
│   └── index.py              # Serverless entry point (main Flask app)
├── public/                   # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css
│   ├── js/
│   └── [other static assets]
├── templates/                # HTML templates
│   ├── index.html
│   ├── prediction.html
│   ├── history.html
│   └── error.html
├── models/                   # ML models (pickle files)
│   ├── random_forest_model.pkl
│   └── scaler.pkl
├── database/                 # Database files (CSV, SQL)
│   ├── agriculture_yield_data.csv
│   └── agriculture.sql
├── vercel.json              # Vercel configuration
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
├── .env.example            # Example env variables
└── .env                    # Environment variables (DO NOT COMMIT)
```

## Step 1: Prerequisites

Before deploying to Vercel, ensure you have:

- ✅ **GitHub Account** - To push your code
- ✅ **Vercel Account** - Free account at https://vercel.com
- ✅ **Git installed** - For version control
- ✅ **Cloud Database** - Choose ONE:
  - PostgreSQL: Supabase, AWS RDS, Google Cloud SQL
  - MySQL: AWS RDS, Azure Database
  - MongoDB: MongoDB Atlas
  - Firebase: Google Firebase (Realtime Database or Firestore)

## Step 2: Database Setup

### Option 1: PostgreSQL with Supabase (Recommended - Free Tier Available)

1. **Sign up at https://supabase.com**
2. **Create a new project**
3. **Get your connection string** from Project Settings → Database
4. **Create tables:**
   ```sql
   CREATE TABLE districts (
       id SERIAL PRIMARY KEY,
       district_name VARCHAR(100) NOT NULL
   );
   
   CREATE TABLE crops (
       id SERIAL PRIMARY KEY,
       crop_name VARCHAR(100) NOT NULL
   );
   
   CREATE TABLE yield_data (
       id SERIAL PRIMARY KEY,
       district_id INTEGER,
       crop_id INTEGER,
       area FLOAT,
       area_unit VARCHAR(20),
       rainfall FLOAT,
       temperature FLOAT,
       soil_ph FLOAT,
       nitrogen FLOAT,
       phosphorus FLOAT,
       potassium FLOAT,
       yield_per_ha FLOAT,
       total_yield FLOAT,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   
   CREATE TABLE chat_history (
       id SERIAL PRIMARY KEY,
       user_message TEXT,
       bot_response LONGTEXT,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       conversation_id VARCHAR(50)
   );
   
   -- Insert sample data
   INSERT INTO districts (district_name) VALUES 
   ('Coimbatore'), ('Chennai'), ('Madurai'), ('Salem'), ('Tiruppur');
   
   INSERT INTO crops (crop_name) VALUES 
   ('Rice'), ('Sugar Cane'), ('Cotton'), ('Ground Nut'), ('Sun Flower');
   ```

5. **Save connection details** - You'll need them for Vercel environment variables

### Option 2: MongoDB with Atlas (Free Tier Available)

1. **Sign up at https://www.mongodb.com/cloud/atlas**
2. **Create a cluster**
3. **Get your connection string** from "Connect to your application"
4. **Keep the URI secure** - Use as environment variable

## Step 3: Local Testing

1. **Copy `.env.example` to `.env`:**
   ```bash
   cp .env.example .env
   ```

2. **Update `.env` with your cloud database credentials:**
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   
   # For PostgreSQL (Supabase):
   DB_HOST=your-project.supabase.co
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_NAME=postgres
   DB_PORT=5432
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run locally:**
   ```bash
   python api/index.py
   ```
   Access at: `http://localhost:3000`

## Step 4: Prepare for GitHub

1. **Initialize Git (if not already done):**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Agricultural Yield Prediction for Vercel"
   ```

2. **Create `.env.example` (NO SECRETS!):**
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   
   # PostgreSQL/Supabase
   DB_HOST=your-db-host
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_NAME=postgres
   DB_PORT=5432
   
   # Or MongoDB
   MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/dbname
   ```

3. **Ensure `.env` is in `.gitignore`:**
   ```
   .env
   .env.local
   .env.*.local
   ```

## Step 5: Push to GitHub

```bash
# Create new repository on GitHub (don't initialize with README)

# Add remote origin (replace with YOUR repo URL)
git remote add origin https://github.com/YOUR_USERNAME/agriculture_yield.git

# Rename branch to main if needed
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 6: Deploy to Vercel

### Method 1: Using Vercel CLI (Recommended)

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy from project directory:**
   ```bash
   vercel
   ```

3. **Follow the prompts:**
   - Link to your GitHub account
   - Select the repository
   - Set environment variables when prompted

### Method 2: Using Vercel Dashboard

1. **Go to https://vercel.com/dashboard**
2. **Click "Add New Project"**
3. **Import from Git** → Select your repository
4. **Configure Project:**
   - Framework: `Other`
   - Root Directory: `.`
   - Build Command: (leave empty)
   - Output Directory: (leave empty)

5. **Add Environment Variables:**
   - Click "Environment Variables"
   - Add each variable from your `.env` file:
     ```
     GEMINI_API_KEY = [your key]
     DB_HOST = [your host]
     DB_USER = [your user]
     DB_PASSWORD = [your password]
     DB_NAME = [your database]
     DB_PORT = [your port]
     ```

6. **Click "Deploy"**

## Step 7: Configure Secrets in Vercel

For sensitive data, use Vercel environment variables:

```bash
# Using CLI
vercel env add GEMINI_API_KEY
vercel env add DB_PASSWORD
# ... etc
```

Production environment variables receive values from Vercel dashboard.

## How to Get Gemini API Key

1. Go to https://aistudio.google.com/
2. Click "Create API Key"
3. Create key for "Google AI Studio"
4. Copy and save the key securely
5. Add to Vercel environment variables

## Testing Your Deployment

After deployment:

1. **Visit your Vercel URL** (e.g., `https://your-app-name.vercel.app`)

2. **Test endpoints:**
   ```
   https://your-app-name.vercel.app/                    # Home page
   https://your-app-name.vercel.app/health              # Health check
   https://your-app-name.vercel.app/predict (POST)      # Predictions
   https://your-app-name.vercel.app/chat (POST/GET)     # AI Chat
   ```

3. **Check logs:**
   ```bash
   vercel logs [deployment-url]
   ```

## Important Notes

### Database Connection on Vercel

The original app uses **localhost MySQL** which won't work on Vercel. You must:

1. ✅ Use a **cloud database service**
2. ✅ Update connection strings in `api/index.py`
3. ✅ Store sensitive credentials in **environment variables only**

### Static Files

- Place static files in `/public` directory
- Vercel automatically serves from `/public`
- Update Flask to point to correct template/static paths

### File Size Limitations

- Vercel Functions timeout after **10 seconds**
- Large file uploads may fail
- Keep model files under 50MB

### Cold Starts

- First request after deployment may be slow (cold start)
- Subsequent requests are faster
- Use Vercel's automatic scaling for production

## Troubleshooting

### "Module not found" error

```bash
# Make sure all imports are in requirements.txt
pip freeze > requirements.txt
```

### Database connection fails

1. Check environment variable names match exactly
2. Ensure database is accessible from Vercel IPs (whitelist `0.0.0.0/0`)
3. Verify credentials are correct
4. Test connection locally first

### Templates not found

Ensure vercel.json has correct routes and Flask template_folder is set to `../templates`

### Slow performance

- Check Vercel function logs for bottlenecks
- Reduce model file size
- Enable Vercel Analytics

## Deployment Checklist

- [ ] DB configured and accessible
- [ ] Gemini API key obtained
- [ ] `.env` file created with correct variables
- [ ] `.gitignore` includes `.env`
- [ ] `.env.example` created (no secrets)
- [ ] Requirements.txt updated
- [ ] Code pushed to GitHub
- [ ] Vercel project created
- [ ] Environment variables set in Vercel
- [ ] Deployment successful
- [ ] Health check endpoint working
- [ ] Prediction endpoint working
- [ ] Chat endpoint working

## Common Environment Variables

```env
# Required
GEMINI_API_KEY=sk-...

# Database (choose one set)
# PostgreSQL
DB_HOST=yourhost.supabase.co
DB_USER=postgres
DB_PASSWORD=***
DB_NAME=postgres
DB_PORT=5432

# MongoDB
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/db

# Optional
FLASK_ENV=production
DEBUG=False
```

## Useful Commands

```bash
# Test locally
python api/index.py

# Push updates
git add .
git commit -m "Your message"
git push origin main

# Redeploy to Vercel
vercel --prod

# Check Vercel deployment status
vercel status

# View logs
vercel logs [url]

# List deployments
vercel list
```

## Support & Resources

- **Vercel Docs:** https://vercel.com/docs
- **Flask Documentation:** https://flask.palletsprojects.com/
- **Google Gemini API:** https://ai.google.dev/
- **Supabase:** https://supabase.com/docs/guides/database
- **MongoDB Atlas:** https://docs.atlas.mongodb.com/

## Next Steps

After successful deployment:

1. Add custom domain (Vercel Dashboard → Settings → Domains)
2. Enable HTTPS (automatic with Vercel)
3. Set up monitoring and alerts
4. Configure backup strategy for database
5. Implement proper error logging
6. Scale database connection pooling if needed

---

**Your agricultural yield prediction system is now live on Vercel!** 🚀🌾
