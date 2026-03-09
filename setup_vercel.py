#!/usr/bin/env python3
"""
Setup script for Vercel deployment
Prepares the project structure for Vercel serverless deployment
"""

import os
import shutil
from pathlib import Path

def setup_vercel_project():
    """Prepare project for Vercel deployment"""
    
    base_path = Path(__file__).parent
    
    print("=" * 60)
    print("🚀 Agricultural Yield Prediction - Vercel Setup")
    print("=" * 60)
    
    # Check if api/index.py exists
    api_path = base_path / 'api' / 'index.py'
    if not api_path.exists():
        print("❌ Error: api/index.py not found!")
        print("   Make sure you've created the api/ folder and index.py file")
        return False
    
    print("✅ api/index.py found")
    
    # Check if vercel.json exists
    vercel_json = base_path / 'vercel.json'
    if not vercel_json.exists():
        print("❌ Error: vercel.json not found!")
        print("   Make sure you've created the vercel.json configuration file")
        return False
    
    print("✅ vercel.json found")
    
    # Check if public directory exists
    public_path = base_path / 'public'
    if not public_path.exists():
        print("📁 Creating /public directory...")
        public_path.mkdir(exist_ok=True)
    else:
        print("✅ /public directory exists")
    
    # Copy static files to public
    static_path = base_path / 'static'
    if static_path.exists():
        print("📋 Copying static files to /public...")
        for item in static_path.rglob('*'):
            if item.is_file():
                relative_path = item.relative_to(static_path)
                dest = public_path / relative_path
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest)
                print(f"   ✓ {relative_path}")
    else:
        print("⚠️  /static directory not found")
    
    # Check templates
    templates_path = base_path / 'templates'
    if templates_path.exists():
        print(f"✅ /templates directory found ({len(list(templates_path.glob('*.html')))} templates)")
    else:
        print("⚠️  /templates directory not found")
    
    # Check models
    models_path = base_path / 'models'
    if models_path.exists():
        pkl_files = list(models_path.glob('*.pkl'))
        if pkl_files:
            print(f"✅ /models directory found ({len(pkl_files)} model files)")
        else:
            print("⚠️  /models directory empty - you need to train models")
    else:
        print("⚠️  /models directory not found")
    
    # Check .env
    env_path = base_path / '.env'
    if env_path.exists():
        print("✅ .env file exists")
    else:
        print("⚠️  .env file not found - copy from .env.example and fill in your values")
    
    # Check requirements.txt
    req_path = base_path / 'requirements.txt'
    if req_path.exists():
        print("✅ requirements.txt found")
    else:
        print("❌ requirements.txt not found")
        return False
    
    # Check .gitignore
    gitignore = base_path / '.gitignore'
    if gitignore.exists():
        print("✅ .gitignore configured")
    else:
        print("⚠️  .gitignore not found")
    
    print("\n" + "=" * 60)
    print("📋 Project Structure Check Complete!")
    print("=" * 60)
    
    print("\n✅ Next Steps:")
    print("1. Fill in your .env file with actual credentials")
    print("2. Test locally: python api/index.py")
    print("3. Push to GitHub: git push origin main")
    print("4. Deploy to Vercel: vercel --prod")
    print("\nDetailed guide: See VERCEL_DEPLOYMENT_GUIDE.md")
    
    return True

if __name__ == '__main__':
    success = setup_vercel_project()
    exit(0 if success else 1)
