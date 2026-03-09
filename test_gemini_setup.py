#!/usr/bin/env python3
"""
Test script for Gemini API integration
Run this to verify your setup before running the Flask app
"""

import os
import sys
from dotenv import load_dotenv

print("=" * 60)
print("🧪 Gemini API Integration Test")
print("=" * 60)

# Load environment variables
print("\n1️⃣  Loading environment variables...")
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

if api_key:
    print("✅ GEMINI_API_KEY found in .env file")
    print(f"   Key (masked): {api_key[:10]}...{api_key[-5:]}")
else:
    print("❌ GEMINI_API_KEY not found in .env file")
    print("   Please add: GEMINI_API_KEY=your_key_here")
    sys.exit(1)

# Try to import google-generativeai
print("\n2️⃣  Checking google-generativeai package...")
try:
    import google.generativeai as genai
    print("✅ google-generativeai imported successfully")
except ImportError:
    print("❌ google-generativeai not installed")
    print("   Run: pip install google-generativeai")
    sys.exit(1)

# Configure Gemini API
print("\n3️⃣  Configuring Gemini API...")
try:
    genai.configure(api_key=api_key)
    print("✅ Gemini API configured successfully")
except Exception as e:
    print(f"❌ Failed to configure Gemini API: {e}")
    sys.exit(1)

# Test API connection
print("\n4️⃣  Testing API connection...")
try:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Hello! This is a test message. Please respond with 'Test successful!'")
    
    if response and response.text:
        print("✅ API connection successful!")
        print(f"   Response: {response.text[:100]}...")
    else:
        print("❌ API returned empty response")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ API test failed: {e}")
    print("   Common issues:")
    print("   - Invalid API key")
    print("   - API key has no quota")
    print("   - Network connection problem")
    print(f"   Error details: {str(e)}")
    sys.exit(1)

# Test Flask integration
print("\n5️⃣  Checking Flask dependencies...")
try:
    import flask
    print(f"✅ Flask {flask.__version__} installed")
except ImportError:
    print("❌ Flask not installed")
    print("   Run: pip install -r requirements.txt")
    sys.exit(1)

# Test database
print("\n6️⃣  Checking database connection...")
try:
    import mysql.connector
    print("✅ mysql-connector-python installed")
    
    # Try to connect to database
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='agriculture_yield'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    conn.close()
    print("✅ Database connection successful")
    
except mysql.connector.Error as e:
    print(f"⚠️  Database connection failed: {e}")
    print("   Make sure MySQL is running and agriculture_yield database exists")
except ImportError:
    print("❌ mysql-connector-python not installed")
    print("   Run: pip install -r requirements.txt")

# Summary
print("\n" + "=" * 60)
print("✅ All tests passed! You're ready to go!")
print("=" * 60)
print("\nNext steps:")
print("1. Run the Flask app: python app.py")
print("2. Open: http://localhost:5000")
print("3. Test the chatbot interface")
print("\nFor detailed setup instructions, see: GEMINI_SETUP.md")
print("=" * 60)
