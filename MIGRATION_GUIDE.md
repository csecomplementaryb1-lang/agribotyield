# 📋 Complete Migration Guide: XAMPP → Vercel

## Overview

This guide explains how to migrate your local Flask application from XAMPP (Apache + localhost MySQL) to Vercel serverless deployment.

## Key Changes

### 1. **Server Architecture**

**BEFORE (XAMPP):**
```
┌─────────────────┐
│   Your Machine  │
├─────────────────┤
│   Apache/PHP    │
│   Flask App     │
│   MySQL (local) │
│   Templates     │
│   Static Files  │
└─────────────────┘
```

**AFTER (Vercel):**
```
┌──────────────────────────────────────┐
│         Vercel Serverless            │
├──────────────────────────────────────┤
│  Function: api/index.py (Flask App)  │
│  Router: Routes requests             │
│  Static: /public files               │
│  DB: Cloud (Supabase/AWS/MongoDB)    │
│  Cache: Edge locations globally      │
└──────────────────────────────────────┘
```

### 2. **File Structure**

**OLD (XAMPP):**
```
app.py                    ← Main app entry point
templates/
  - index.html
  - prediction.html
static/
  - css/
  - js/
models/
  - *.pkl
requirements.txt
.env
```

**NEW (Vercel):**
```
api/
  - index.py              ← Serverless entry point (MOVED)
templates/                ← UNCHANGED
  - index.html
  - prediction.html
public/                   ← NEW (replaces /static)
  - css/
  - js/
models/
  - *.pkl
vercel.json               ← NEW (Vercel config)
requirements.txt          ← UPDATED
.gitignore               ← UPDATED
.env.example             ← NEW (for documentation)
.env                     ← UNCHANGED (but referenced differently)
```

### 3. **Code Changes**

#### Database Connection

**BEFORE:**
```python
# Direct localhost MySQL
db = mysql.connector.connect(
    host='localhost',      # ❌ Won't work on Vercel
    user='root',
    password='',
    database='agriculture_yield'
)
```

**AFTER:**
```python
# Cloud database via environment variables
db = psycopg2.connect(
    host=os.getenv('DB_HOST'),        # ✅ From Vercel env vars
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    port=os.getenv('DB_PORT', 5432)
)
```

#### Environment Variables

**BEFORE:**
```python
from dotenv import load_dotenv
load_dotenv()  # Reads from .env file
api_key = os.getenv('GEMINI_API_KEY')
```

**AFTER:**
```python
import os
# Vercel provides env vars automatically
api_key = os.getenv('GEMINI_API_KEY')  # ✅ No load_dotenv needed
```

#### Flask App Export

**BEFORE:**
```python
if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
```

**AFTER:**
```python
# No main block - Vercel imports the app object directly
# app is available for Vercel to instantiate
```

#### Template Folder Paths

**BEFORE:**
```python
app = Flask(__name__)  # Auto-finds templates/ in current dir
```

**AFTER:**
```python
# Specify absolute paths for Vercel
app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
```

### 4. **Dependency Changes**

**ADDED:**
- `Werkzeug==2.3.7` - WSGI compatibility

**REMOVED (Optional):**
- `python-dotenv` - Not needed (though kept for development)
- `mysql-connector-python` - Replace with cloud DB driver

**ADDED (Choose One):**
- PostgreSQL: `psycopg2-binary==2.9.9`
- MongoDB: `pymongo==4.5.0`
- Cloud SQL: `google-cloud-sql-connector==1.4.0`

## Step-by-Step Migration

### Phase 1: Local Setup (Before GitHub)

#### 1.1 Create New Directory Structure

```bash
# Create api/ and public/ directories
mkdir api
mkdir public
```

#### 1.2 Create api/index.py

Copy your app.py to api/index.py and update:
- Template paths: `template_folder='../templates'`
- Static paths: `static_folder='../static'`
- Database connections: Use cloud DB credentials from env vars

#### 1.3 Update Configuration Files

```bash
# Create vercel.json
cat > vercel.json << 'EOF'
{
  "version": 2,
  "builds": [{"src": "api/index.py", "use": "@vercel/python"}],
  "routes": [
    {"src": "/(.*)", "dest": "api/index.py"}
  ]
}
EOF
```

#### 1.4 Copy Static Files

```bash
# Copy CSS, JS, images to public/
cp -r static/* public/
```

#### 1.5 Update requirements.txt

```bash
# Remove mysql-connector-python (won't work on Vercel)
# Add cloud database driver
# Add Werkzeug for WSGI
```

#### 1.6 Test Locally

```bash
# Update .env with real cloud DB credentials
python api/index.py

# Visit http://localhost:3000
```

### Phase 2: Version Control (GitHub)

```bash
# Initialize git (if not done)
git init

# Add all files except .env
git add .
git commit -m "Initial Vercel setup"

# Create new repository on GitHub (don't init with README)

# Add remote and push
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### Phase 3: Vercel Deployment

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

During deploy, Vercel will:
1. Ask to link GitHub repo
2. Set environment variables
3. Install dependencies from requirements.txt
4. Build serverless functions
5. Deploy to Vercel edge network
6. Return your production URL

### Phase 4: Post-Deployment

1. **Verify Health Check**
   ```bash
   curl https://your-app.vercel.app/health
   ```

2. **Check Logs**
   ```bash
   vercel logs https://your-app.vercel.app
   ```

3. **Test Core Features**
   - Home page loads
   - Prediction form works
   - Chat responds
   - History displays

## Database Migration Checklist

### From MySQL to Cloud Database

**Step 1: Export Schema**
```bash
# Export your MySQL database
mysqldump -h localhost -u root agriculture_yield > backup.sql
```

**Step 2: Create Cloud Database**
- Supabase: https://supabase.com
- AWS RDS: https://aws.amazon.com/rds/
- MongoDB Atlas: https://www.mongodb.com/cloud/atlas

**Step 3: Import Data**
```bash
# For PostgreSQL (Supabase)
psql -h your-host.supabase.co -U postgres -d postgres < backup.sql
```

**Step 4: Update Connection String**
```env
# .env
DB_HOST=your-host.supabase.co
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_NAME=postgres
DB_PORT=5432
```

**Step 5: Test Connection**
```python
# Test script
import psycopg2
import os
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)
print("✅ Connected!")
```

## Troubleshooting Migration Issues

### Issue: "Cannot find app object"

**Cause:** Vercel can't import Flask app from api/index.py

**Fix:**
```python
# Make sure api/index.py has:
from flask import Flask
app = Flask(__name__)  # Must be named 'app'
# ... routes ...
# NO: if __name__ == '__main__':
```

### Issue: "Templates not found"

**Cause:** Flask looking in wrong directory

**Fix:**
```python
app = Flask(__name__, 
            template_folder='../templates')  # Relative to api/index.py
```

### Issue: "Database connection refused"

**Cause:** Localhost database, cloud DB credentials missing, or firewall

**Fix:**
1. Check DB_HOST is cloud URL, not localhost
2. Verify credentials in Vercel env vars
3. Whitelist Vercel IPs in database firewall

### Issue: "Module not found"

**Cause:** Package not in requirements.txt

**Fix:**
```bash
pip freeze > requirements.txt
# Remove local paths, keep only package==version
git add requirements.txt
git commit -m "Update requirements"
git push
vercel --prod  # Redeploy
```

### Issue: Function timeout

**Cause:** Request takes >10 seconds on Vercel

**Fix:**
- Optimize database queries
- Cache database results
- Reduce model file sizes
- Use serverless databases with auto-scaling

## Performance Tips for Migration

### 1. Optimize Database

```sql
-- Add indexes on frequently queried columns
CREATE INDEX idx_yield_district ON yield_data(district_id);
CREATE INDEX idx_yield_crop ON yield_data(crop_id);
CREATE INDEX idx_chat_conversation ON chat_history(conversation_id);
```

### 2. Cache Static Files

```python
@app.after_request
def set_cache_headers(response):
    response.headers['Cache-Control'] = 'max-age=31536000'  # 1 year
    return response
```

### 3. Minimize Model Size

```python
# Use model compression
import pickle

with open('models/model.pkl', 'wb') as f:
    pickle.dump(model, f, protocol=pickle.HIGHEST_PROTOCOL)
```

### 4. Use Connection Pooling

```python
from psycopg2 import pool

connection_pool = pool.SimpleConnectionPool(2, 10,
                                          host=os.getenv('DB_HOST'),
                                          user=os.getenv('DB_USER'),
                                          password=os.getenv('DB_PASSWORD'))
```

## Testing Before Pushing to Production

```bash
# 1. Local testing
python api/index.py

# 2. Test all endpoints
curl http://localhost:3000/
curl http://localhost:3000/health
curl -X POST http://localhost:3000/predict

# 3. Check for errors
# Review console output for warnings

# 4. Test environment variables
python -c "import os; print(os.getenv('GEMINI_API_KEY'))"

# 5. Verify database connection
python api/index.py  # Should show "✅ Database connected"

# 6. Only then push to GitHub
git push origin main
```

## Rollback Plan

If deployment has issues:

```bash
# Redeploy previous version
vercel rollback

# Or redeploy current
vercel --prod

# Check current deployment
vercel list

# View logs for debugging
vercel logs [url]
```

## Summary

| Aspect | XAMPP | Vercel |
|--------|-------|--------|
| Monthly Cost | $0 (your machine) | Free tier / $20+ Pro |
| Uptime | While your PC on | 99.95% SLA |
| Deployment | Manual (XAMPP) | Automated (GitHub push) |
| Database | Localhost | Cloud (Supabase/AWS) |
| Scaling | Manual | Automatic |
| HTTPS | Manual setup | Built-in |
| Environment | Windows/Mac/Linux | Isolated container |
| Cold Starts | N/A | ~1-2s first request |
| Maintenance | Your responsibility | Vercel manages |

---

**Congratulations!** Your agricultural yield prediction system is now ready for the cloud! 🚀🌾
