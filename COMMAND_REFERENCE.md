# 🔧 Command Reference: XAMPP to Vercel Deployment

## Quick Command Cheat Sheet

### 📦 Prerequisites Setup

```bash
# Install Node.js and npm (if not installed)
# Download from https://nodejs.org/

# Install Vercel CLI globally
npm install -g vercel

# Verify installation
vercel --version
node --version
npm --version
```

### 🏗️ Project Setup

```bash
# Navigate to project directory
cd path/to/agriculture_yield

# Create API folder structure (Windows)
mkdir api
mkdir public

# Create API folder structure (Mac/Linux)
mkdir -p api public

# Initialize git (if not already)
git init

# Check git status
git status
```

### 🔐 Environment Variables

```bash
# Copy environment template (Windows)
copy .env.example .env

# Copy environment template (Mac/Linux)
cp .env.example .env

# Edit .env file with your values
# Windows: Open with Notepad
notepad .env

# Mac/Linux: Use preferred editor
nano .env
# or
vi .env
```

### 📝 Setup & Testing

```bash
# Run setup verification script
python setup_vercel.py

# Install Python dependencies
pip install -r requirements.txt

# Test locally
python api/index.py

# Kill local server (if needed)
# Windows: Press Ctrl+C
# Mac/Linux: Press Ctrl+C
```

### 🌐 Git Commands (Version Control)

```bash
# Stage all files except .env
git add .
git add -A

# Review staged files
git status

# Commit changes
git commit -m "Initial commit: Agricultural Yield Prediction for Vercel"

# View commit history
git log --oneline

# Undo last commit (if needed)
git reset --soft HEAD~1

# Create GitHub repository
# 1. Go to https://github.com/new
# 2. Create empty repository (no README)
# 3. Copy the remote URL

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/agriculture_yield.git

# Rename branch to main (if using older git)
git branch -M main

# Push to GitHub
git push -u origin main

# Future pushes (after first time)
git push origin main

# Check remote
git remote -v
```

### 🚀 Vercel Deployment

```bash
# Login to Vercel
vercel login

# Deploy to preview (testing)
vercel

# Deploy to production
vercel --prod

# List all deployments
vercel list

# View specific deployment logs
vercel logs your-app-name.vercel.app

# Check deployment status
vercel status

# Rollback to previous deployment
vercel rollback

# Redeploy current
vercel --prod --force

# View live deployment
vercel --prod
```

### ⚙️ Environment Variables in Vercel

```bash
# Add env variable via CLI
vercel env add GEMINI_API_KEY
# Then enter your key when prompted

# List all environment variables
vercel secrets ls

# Remove environment variable
vercel secrets remove GEMINI_API_KEY

# Set multiple variables (interactive)
# Go to Vercel Dashboard → Project → Settings → Environment Variables
# Click "Add New" for each variable
```

### 🔍 Debugging & Testing

```bash
# Test health endpoint
curl https://your-app.vercel.app/health

# Test with JSON (chat endpoint)
curl -X POST https://your-app.vercel.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello"}'

# View real-time logs
vercel logs your-app.vercel.app --follow

# View specific function logs
vercel logs your-app.vercel.app --query=function

# Check function runtime
vercel logs your-app.vercel.app --function=api/index.py
```

### 📊 Database Commands

```bash
# PostgreSQL (Supabase) - Test connection
psql -h your-host.supabase.co -U postgres -d postgres -c "SELECT version();"

# MongoDB - Test connection
mongosh "mongodb+srv://user:password@cluster.mongodb.net/dbname"

# Export database
mysqldump -h localhost -u root agriculture_yield > backup.sql

# Backup to file
pg_dump -h your-host -U postgres -d database > backup.sql
```

### 🐛 Troubleshooting Commands

```bash
# Check Python version
python --version
python3 --version

# Check if package is installed
pip show google-generativeai
pip list | findstr google  # Windows
pip list | grep google     # Mac/Linux

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# Clear pip cache
pip cache purge

# Check current Git status
git status

# Show git log
git log --graph --oneline --all

# Reset to last commit (discard changes)
git reset --hard HEAD

# Check environment variables
echo %GEMINI_API_KEY%           # Windows
echo $GEMINI_API_KEY            # Mac/Linux

# Verify .env file
cat .env                        # Mac/Linux
type .env                       # Windows
```

### 📁 File Operations

```bash
# Navigate directories
cd agriculture_yield
cd api
cd ..

# List files in directory
ls                              # Mac/Linux
dir                             # Windows
dir /s                          # Windows (recursive)

# View file contents
cat filename.py                 # Mac/Linux
type filename.py                # Windows

# Copy files
cp source.py dest.py            # Mac/Linux
copy source.py dest.py          # Windows

# Move files
mv source.py dest/              # Mac/Linux
move source.py dest\            # Windows

# Create file
touch filename.py               # Mac/Linux
type nul > filename.py          # Windows
```

### 📈 Production Monitoring

```bash
# View all deployments
vercel list --limit=20

# Get deployment URL
vercel ls | grep "agriculture" 

# Monitor function metrics
# Visit: Vercel Dashboard → Project → Deployments → Analytics

# Check error logs
vercel logs your-app.vercel.app --error

# Performance metrics
vercel analytics integration setup
```

### 🔄 CI/CD Pipeline (After Initial Setup)

```bash
# Make changes locally
git add .
git commit -m "Fix navigation bug"
git push origin main

# Vercel auto-deploys on GitHub push!
# No need to run 'vercel' command each time

# Monitor deployment
vercel list --limit=1
```

### 🧹 Cleanup Commands

```bash
# Remove build files
rm -rf __pycache__              # Mac/Linux
rmdir /s __pycache__            # Windows

# Clean Python cache
find . -type d -name __pycache__ -exec rm -r {} +  # Mac/Linux
pip cache purge

# Remove old deployments (keep last 10)
vercel remove --safe

# Delete environment variable
vercel env rm VARIABLE_NAME
```

### 🆘 Emergency Commands

```bash
# If something breaks, revert to previous state
git reset --hard origin/main
git pull origin main

# Clear Vercel cache and redeploy
vercel build --prod --no-cache
vercel --prod --force

# Full reset (only if necessary!)
git reset --hard HEAD~1
git push --force origin main
```

## 🎯 Command Order for Fresh Deployment

```bash
# 1. One-time setup
git init
git remote add origin https://github.com/USERNAME/REPO.git

# 2. Create project locally
cp .env.example .env
# Edit .env with your values

# 3. Test locally
python api/index.py
# Visit http://localhost:3000

# 4. Push to GitHub
git add .
git commit -m "Initial Vercel setup"
git push -u origin main

# 5. Deploy to Vercel
vercel --prod

# 6. Monitor
vercel logs your-app.vercel.app

# 7. Future updates
git add .
git commit -m "Your changes"
git push origin main
# Auto-deployed by Vercel!
```

## 💡 Pro Tips

```bash
# Use git aliases for quick commands
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status

# Usage:
git st              # instead of git status
git ci -m "msg"     # instead of git commit -m
git co main         # instead of git checkout main

# Keep .env secure - never commit!
echo ".env" >> .gitignore
git rm --cached .env
git commit -m "Remove .env from version control"

# View actual environment variables being used
python -c "import os; print({k: v for k, v in os.environ.items() if 'DB' in k or 'GEMINI' in k})"

# Useful zsh/bash aliases (add to ~/.bashrc or ~/.zshrc)
alias deploy='git add . && git commit -m "Deploy" && git push origin main'
alias logs='vercel logs'
alias status='vercel status'
```

## 📚 Common Command Combinations

```bash
# Complete setup from scratch
mkdir agriculture_yield && cd agriculture_yield
git init
cp .env.example .env
# (edit .env)
python setup_vercel.py
python api/index.py
git add .
git commit -m "Initial setup"
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main
npm install -g vercel
vercel --prod

# Quick update and redeploy
git add .
git commit -m "Update"
git push origin main
# Vercel auto-deploys!
vercel logs your-app.vercel.app

# Troubleshoot and redeploy
pip install -r requirements.txt --upgrade
python api/index.py  # Test
git add requirements.txt
git commit -m "Update dependencies"
git push origin main
vercel logs your-app.vercel.app
```

---

**Remember:** When in doubt, check logs first! `vercel logs your-app.vercel.app`
