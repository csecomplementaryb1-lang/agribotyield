#!/usr/bin/env python3
"""
List available Gemini models to find the correct model name
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

print("=" * 60)
print("📋 Listing Available Gemini Models")
print("=" * 60)

# Load environment variables
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("❌ GEMINI_API_KEY not found in .env file")
    exit(1)

print(f"\n✅ API Key loaded: {api_key[:10]}...{api_key[-5:]}")

# Configure Gemini API
genai.configure(api_key=api_key)

print("\n🔍 Fetching available models...\n")

try:
    # List all available models
    models = genai.list_models()
    
    print("Available Gemini Models:")
    print("-" * 60)
    
    available_models = []
    for model in models:
        model_name = model.name
        # Extract just the model ID (remove 'models/' prefix)
        model_id = model_name.replace('models/', '')
        available_models.append(model_id)
        
        # Check if model supports generateContent
        supported_methods = getattr(model, 'supported_generation_methods', [])
        supports_generate = 'generateContent' in supported_methods
        
        status = "✅" if supports_generate else "⚠️"
        print(f"{status} {model_id}")
        if supported_methods:
            print(f"   Methods: {', '.join(supported_methods)}")
    
    print("\n" + "=" * 60)
    print(f"📊 Total models found: {len(available_models)}")
    print("=" * 60)
    
    # Find a suitable model (prefer flash or pro)
    print("\n💡 Recommended models:")
    for model_id in available_models:
        if 'flash' in model_id.lower() and 'generateContent' in str(models):
            print(f"   • {model_id} (fast & capable)")
        elif 'pro' in model_id.lower():
            print(f"   • {model_id} (powerful)")
    
    print("\n✅ Copy one of the model names above and use it in app.py")
    print("   Example: model = genai.GenerativeModel('your-model-name-here')")
    
except Exception as e:
    print(f"❌ Error listing models: {e}")
    print(f"\nError details: {str(e)}")
    print("\nTroubleshooting:")
    print("1. Verify your API key is valid")
    print("2. Check that API key has quota enabled")
    print("3. Try visiting: https://aistudio.google.com/")
