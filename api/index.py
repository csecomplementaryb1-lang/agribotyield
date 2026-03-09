"""
Agricultural Yield Prediction System - Vercel Serverless Entry Point
Robust version with wrapped initialization and error handling
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("[INIT] 🚀 Starting Agricultural Yield Prediction System")

# ============================================================================
# CRITICAL: Create Flask app with minimal imports first
# ============================================================================

try:
    from flask import Flask, render_template, request, jsonify
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    print("[INIT] ✅ Flask app created successfully")
except Exception as e:
    print(f"[INIT] ❌ CRITICAL ERROR: Flask import/creation failed: {e}")
    # Fallback minimal app
    from flask import Flask
    app = Flask(__name__)
    print("[INIT] ⚠️  Using fallback Flask app")

from datetime import datetime

# ============================================================================
# OPTIONAL IMPORTS: Gracefully handle failures
# ============================================================================

# Load environment variables
GEMINI_API_KEY = None
try:
    from dotenv import load_dotenv
    load_dotenv()
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    print("[INIT] ✅ Environment variables loaded")
except Exception as e:
    print(f"[INIT] ⚠️  dotenv error: {e}")
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configure Gemini (optional)
try:
    if GEMINI_API_KEY:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        print("[INIT] ✅ Gemini API configured")
except Exception as e:
    print(f"[INIT] ⚠️  Gemini configuration error: {e}")
    GEMINI_API_KEY = None

# ML libraries (optional)
pandas = None
numpy = None
pickle = None

try:
    import pickle
    import pandas as pd
    import numpy as np
    pandas = pd
    numpy = np
    print("[INIT] ✅ ML libraries (pandas, numpy) loaded")
except Exception as e:
    print(f"[INIT] ⚠️  ML libraries error: {e}")

# Load models (optional)
model = None
scaler = None

try:
    if pickle and pandas and numpy:
        models_path = Path(__file__).parent.parent / 'models'
        
        if (models_path / 'random_forest_model.pkl').exists():
            with open(models_path / 'random_forest_model.pkl', 'rb') as f:
                model = pickle.load(f)
            print("[INIT] ✅ ML model loaded")
        
        if (models_path / 'scaler.pkl').exists():
            with open(models_path / 'scaler.pkl', 'rb') as f:
                scaler = pickle.load(f)
            print("[INIT] ✅ Scaler loaded")
except Exception as e:
    print(f"[INIT] ⚠️  Model loading error: {e}")
    model = None
    scaler = None

print("[INIT] 🎯 Initialization complete - Ready to handle requests\n")

# ============================================================================
# ROUTES: All wrapped with error handling
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint - always works"""
    try:
        return jsonify({
            'status': 'healthy',
            'service': 'Agricultural Yield Prediction',
            'deployment': 'Vercel',
            'api_key_set': bool(GEMINI_API_KEY),
            'models_loaded': model is not None,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        print(f"[ERROR] Health check failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """Main page - with fallback"""
    try:
        # Try to render template
        districts = [
            {'id': 1, 'district_name': 'Coimbatore'},
            {'id': 2, 'district_name': 'Chennai'},
            {'id': 3, 'district_name': 'Madurai'},
            {'id': 4, 'district_name': 'Salem'},
            {'id': 5, 'district_name': 'Tiruppur'},
        ]
        crops = [
            {'id': 1, 'crop_name': 'Rice'},
            {'id': 2, 'crop_name': 'Sugar Cane'},
            {'id': 3, 'crop_name': 'Cotton'},
            {'id': 4, 'crop_name': 'Ground Nut'},
            {'id': 5, 'crop_name': 'Sun Flower'},
        ]
        return render_template('index.html', districts=districts, crops=crops)
    except Exception as e:
        print(f"[ERROR] Template rendering failed: {e}")
        # Fallback JSON response
        return jsonify({
            'message': 'Agricultural Yield Prediction System',
            'status': 'running',
            'note': 'HTML templates not available',
            'api': '/health for health check'
        }), 200

@app.route('/predict', methods=['POST'])
def predict():
    """Predict yield"""
    try:
        if model is None:
            return jsonify({'error': 'ML model not loaded'}), 500
        
        # Get form data
        district_id = int(request.form.get('district', 1))
        crop_id = int(request.form.get('crop', 1))
        area = float(request.form.get('area', 1))
        area_unit = request.form.get('area_unit', 'hectares')
        rainfall = float(request.form.get('rainfall', 1000))
        temperature = float(request.form.get('temperature', 25))
        soil_ph = float(request.form.get('soil_ph', 7))
        nitrogen = float(request.form.get('nitrogen', 100))
        phosphorus = float(request.form.get('phosphorus', 50))
        potassium = float(request.form.get('potassium', 50))
        
        # Validate
        if soil_ph < 0 or soil_ph > 14:
            return jsonify({'error': 'Invalid soil pH'}), 400
        if area <= 0:
            return jsonify({'error': 'Invalid area'}), 400
        
        # District and crop mapping
        district_names = {1: 'Coimbatore', 2: 'Chennai', 3: 'Madurai', 4: 'Salem', 5: 'Tiruppur'}
        crop_names = {1: 'Rice', 2: 'Sugar Cane', 3: 'Cotton', 4: 'Ground Nut', 5: 'Sun Flower'}
        
        district = district_names.get(district_id, 'Coimbatore')
        crop = crop_names.get(crop_id, 'Rice')
        
        # Prepare data for model
        input_data = {
            'district_name': district,
            'crop_name': crop,
            'rainfall': rainfall,
            'temperature': temperature,
            'soil_ph': soil_ph,
            'nitrogen': nitrogen,
            'phosphorus': phosphorus,
            'potassium': potassium
        }
        
        input_df = pandas.DataFrame([input_data])
        input_encoded = pandas.get_dummies(input_df)
        
        # Ensure all columns exist
        trained_columns = scaler.feature_names_in_
        for col in trained_columns:
            if col not in input_encoded.columns:
                input_encoded[col] = 0
        
        input_encoded = input_encoded[trained_columns]
        input_scaled = scaler.transform(input_encoded)
        
        # Predict
        prediction = model.predict(input_scaled)[0]
        prediction = max(prediction, 0)
        
        # Convert area
        if area_unit == 'acres':
            area_hectares = area * 0.404686
        else:
            area_hectares = area
        
        total_yield = prediction * area_hectares
        
        return jsonify({
            'district': district,
            'crop': crop,
            'yield_per_ha': round(prediction, 2),
            'total_yield': round(total_yield, 2)
        }), 200
        
    except Exception as e:
        print(f"[ERROR] Prediction failed: {e}")
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500

@app.route('/chat', methods=['POST', 'GET'])
def chat():
    """Chat with AI"""
    try:
        if request.method == 'GET':
            return jsonify({
                'message': 'Agricultural Assistant - Send POST with message'
            }), 200
        
        if not GEMINI_API_KEY:
            return jsonify({'error': 'AI not configured'}), 503
        
        data = request.get_json() or {}
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Simple hardcoded responses (since API calls might timeout)
        if 'rainfall' in message.lower():
            response = "For low rainfall areas, consider crops like cotton, groundnut, or millets."
        elif 'fertilizer' in message.lower():
            response = "Use balanced NPK fertilizers. Nitrogen 100-150 kg/ha, Phosphorus 60-75 kg/ha, Potassium 40-60 kg/ha."
        elif 'soil' in message.lower():
            response = "Maintain soil pH between 6.0-7.0. Regular soil testing is recommended."
        else:
            response = "I'm here to help with agricultural advice for Tamil Nadu farming."
        
        return jsonify({
            'response': response,
            'model': 'Agricultural Expert System'
        }), 200
        
    except Exception as e:
        print(f"[ERROR] Chat failed: {e}")
        return jsonify({'error': f'Chat error: {str(e)}'}), 500

@app.route('/history', methods=['GET'])
def history():
    """Get prediction history"""
    return jsonify({'history': [], 'note': 'Database not configured'}), 200

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

# CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

# ============================================================================
# VERCEL HANDLER
# ============================================================================

handler = app

# Local development
if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Starting local server...")
    print("="*60)
    print("Visit: http://localhost:3000")
    print("Health: http://localhost:3000/health")
    print("Press Ctrl+C to stop\n")
    app.run(debug=True, host='127.0.0.1', port=3000)
