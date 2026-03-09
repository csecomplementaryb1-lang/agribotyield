"""
Agricultural Yield Prediction System - Vercel Serverless Entry Point
This is the main entry point for Vercel deployment.
The Flask app is exported as 'app' for Vercel to serve.
"""

from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv
import google.generativeai as genai
import sys
from pathlib import Path

# Add parent directory to path so we can import from modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    print("✅ Gemini API configured successfully!")
else:
    print("⚠️  Gemini API key not found in environment variables")

# Load trained model and scaler
model = None
scaler = None
try:
    models_path = Path(__file__).parent.parent / 'models'
    with open(models_path / 'random_forest_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open(models_path / 'scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    print("✅ ML models loaded successfully!")
except Exception as e:
    print(f"⚠️  Model loading error: {e}")
    print("Models will be unavailable until trained")

# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================

def get_db_connection():
    """
    Create database connection.
    
    NOTE: For Vercel deployment, you MUST use a cloud database service:
    - Google Cloud SQL
    - AWS RDS
    - Supabase PostgreSQL
    - MongoDB Atlas
    - Firebase
    
    Localhost databases won't work on Vercel.
    Update the connection details below with your cloud database credentials
    from environment variables.
    """
    try:
        # Example for PostgreSQL via Supabase or similar:
        # import psycopg2
        # return psycopg2.connect(
        #     host=os.getenv('DB_HOST'),
        #     user=os.getenv('DB_USER'),
        #     password=os.getenv('DB_PASSWORD'),
        #     database=os.getenv('DB_NAME'),
        #     port=os.getenv('DB_PORT', 5432)
        # )
        
        # For now, returning None - database operations will be limited
        print("⚠️  Database not configured for Vercel deployment")
        return None
        
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def check_database_tables():
    """Check if required tables exist and have data"""
    conn = get_db_connection()
    if conn is None:
        print("⚠️  Database not available - skipping table check")
        return False
    
    # Implementation would go here for actual database
    return True

def create_chat_history_table():
    """Create chat_history table if it doesn't exist"""
    try:
        conn = get_db_connection()
        if conn is None:
            print("⚠️  Cannot create chat history table - database not connected")
            return False
        # Implementation would go here
        return True
    except Exception as e:
        print(f"⚠️  Error creating chat history table: {e}")
        return False

def store_chat_history(user_message, bot_response, conversation_id=None):
    """Store chat messages in database"""
    try:
        conn = get_db_connection()
        if conn is None:
            # Store in memory or log instead
            return False
        # Implementation would go here
        return True
    except Exception as e:
        print(f"⚠️  Error storing chat history: {e}")
        return False

def get_chat_history(conversation_id=None, limit=10):
    """Retrieve chat history from database"""
    try:
        conn = get_db_connection()
        if conn is None:
            return []
        # Implementation would go here
        return []
    except Exception as e:
        print(f"⚠️  Error retrieving chat history: {e}")
        return []

def store_prediction_in_db(district_id, crop_id, area, area_unit, rainfall, temperature,
                          soil_ph, nitrogen, phosphorus, potassium, yield_per_ha, total_yield):
    """Store the prediction in database for historical records"""
    try:
        conn = get_db_connection()
        if conn is None:
            print("⚠️  Database not connected - prediction not stored")
            return False
        # Implementation would go here
        return True
    except Exception as e:
        print(f"⚠️  Error storing prediction: {e}")
        return False

# ============================================================================
# AI RESPONSE FUNCTIONS
# ============================================================================

def get_gemini_response(user_message, conversation_history=None):
    """
    Get response from Google Gemini API with conversation context
    """
    try:
        if not GEMINI_API_KEY:
            return get_fallback_response(user_message)
        
        model_obj = genai.GenerativeModel('gemini-2.5-flash')
        
        system_prompt = """You are an agricultural expert specializing in Tamil Nadu farming practices. 
You have deep knowledge about:
- Crop selection for different Tamil Nadu districts
- Soil management and fertilization strategies
- Irrigation and water management techniques
- Pest and disease control methods
- Yield optimization techniques
- Climate-resilient farming practices
- Organic farming methods
- Government schemes and subsidies for farmers
- Sustainable agriculture practices
- Crop rotation and intercropping strategies

When responding:
1. Always be specific to Tamil Nadu conditions and local practices
2. Provide actionable, practical recommendations
3. Use metric units (kg/ha, mm, °C, etc.)
4. Reference local terminology familiar to Tamil Nadu farmers
5. Be concise but informative (keep responses under 500 words)
6. Use relevant emojis to make responses engaging
7. If asked about something outside agriculture, politely redirect to farming topics
8. If unsure, suggest consulting with local agricultural officers or extension services

Current context: This is an agricultural yield prediction system for Tamil Nadu."""

        # Build conversation context
        messages = []
        if conversation_history:
            for item in conversation_history[-3:]:  # Keep last 3 exchanges
                messages.append({
                    'role': 'user',
                    'parts': [item.get('user_message', '')]
                })
                messages.append({
                    'role': 'model',
                    'parts': [item.get('bot_response', '')]
                })
        
        # Add current user message
        messages.append({
            'role': 'user',
            'parts': [user_message]
        })
        
        print(f"🤖 Sending request to Gemini API: {user_message[:100]}...")
        
        chat = model_obj.start_chat(history=[])
        response = chat.send_message(system_prompt)
        response = chat.send_message(user_message)
        ai_response = response.text
        
        print(f"✅ Gemini API response received: {len(ai_response)} characters")
        return ai_response
        
    except Exception as e:
        print(f"⚠️  Gemini API error: {e}")
        return get_fallback_response(user_message)

def get_fallback_response(user_message):
    """Fallback responses if Gemini API fails"""
    print("🔄 Using fallback response system...")
    
    agricultural_knowledge = {
        "best crops for low rainfall": """🌾 **Best Crops for Low Rainfall Areas in Tamil Nadu (500-700mm):**

**Recommended Crops:**
• **Ground Nut** (requires 500-600mm) - Suitable for Krishnagiri, Dharmapuri
• **Sun Flower** (drought-tolerant) - Grows well in Coimbatore, Madurai  
• **Cotton** (needs 500-700mm) - Ideal for Salem, Tiruppur
• **Millets** (Ragi, Cholam) - Traditional drought-resistant crops

**💡 Water Conservation Tips:**
- Use drip irrigation systems
- Practice mulching to conserve moisture
- Choose short-duration varieties
- Implement rainwater harvesting""",

        "improve soil fertility for rice": """🌱 **Improving Soil Fertility for Rice in Tamil Nadu:**

**1. Organic Matter Management:**
   - Farmyard manure: 10-12 tons/ha
   - Green manure: Grow sunnhemp or daincha
   - Compost: 5-6 tons/ha

**2. Balanced Fertilization:**
   - Nitrogen: 120-150 kg/ha (3 splits)
   - Phosphorus: 60-75 kg/ha (basal dose)
   - Potassium: 40-60 kg/ha

**3. Soil Health:**
   - Maintain pH 6.0-7.0
   - Zinc sulfate: 25 kg/ha for deficient soils
   - Regular soil testing every 2-3 years""",

        "fertilizer for sugarcane": """🎋 **Sugarcane Fertilizer Management in Tamil Nadu:**

**Recommended Dosage (per hectare):**
• Nitrogen: 275-300 kg (4-5 splits)
• Phosphorus: 62.5 kg (basal dose)  
• Potassium: 112.5 kg

**Application Schedule:**
1. **Basal**: 1/4 N + full P + full K at planting
2. **30-35 days**: 1/4 N (first irrigation)
3. **60-65 days**: 1/4 N (grand growth phase)
4. **90-95 days**: 1/4 N (final dose)

**Additional:**
• Farmyard manure: 25 tons/ha before planting
• Use fertigation for better efficiency""",

        "general advice": """🤖 **Agricultural Assistant**

I can help you with:

🌿 **Crop Management:**
• Crop selection based on soil and climate
• Fertilizer recommendations  
• Pest and disease management
• Irrigation scheduling

🌱 **Soil & Inputs:**
• Soil testing interpretation
• Nutrient management
• Organic farming practices

📊 **Planning & Analysis:**
• Cost-benefit analysis
• Climate information

Please ask specific questions about your farming needs! 🚜"""
    }
    
    user_lower = user_message.lower()
    
    if any(keyword in user_lower for keyword in ['rainfall', 'low rain', 'dry area', 'drought']):
        return agricultural_knowledge["best crops for low rainfall"]
    elif any(keyword in user_lower for keyword in ['soil', 'fertility', 'rice', 'paddy']):
        return agricultural_knowledge["improve soil fertility for rice"]
    elif any(keyword in user_lower for keyword in ['fertilizer', 'sugarcane']):
        return agricultural_knowledge["fertilizer for sugarcane"]
    else:
        return agricultural_knowledge["general advice"]

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    """Main page with prediction form"""
    # Sample data for dropdowns (replace with database query when configured)
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

@app.route('/predict', methods=['POST'])
def predict():
    """Handle yield prediction requests"""
    try:
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
        
        # Validate inputs
        if soil_ph < 0 or soil_ph > 14:
            return "Error: Soil pH must be between 0 and 14"
        if area <= 0:
            return "Error: Area must be greater than 0"
        if rainfall < 0:
            return "Error: Rainfall cannot be negative"
        
        # Convert area to hectares for calculation
        if area_unit == 'acres':
            area_hectares = area * 0.404686
        else:
            area_hectares = area
        
        # Get district and crop names
        district_names = {1: 'Coimbatore', 2: 'Chennai', 3: 'Madurai', 4: 'Salem', 5: 'Tiruppur'}
        crop_names = {1: 'Rice', 2: 'Sugar Cane', 3: 'Cotton', 4: 'Ground Nut', 5: 'Sun Flower'}
        
        district = district_names.get(district_id, 'Coimbatore')
        crop = crop_names.get(crop_id, 'Rice')
        
        # Prepare input data for ML model
        if model is None or scaler is None:
            # If model not loaded, return error
            return render_template('error.html', 
                                   error="ML model not available. Please ensure models are trained and deployed.")
        
        try:
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
            
            input_df = pd.DataFrame([input_data])
            input_encoded = pd.get_dummies(input_df)
            
            trained_columns = scaler.feature_names_in_
            for col in trained_columns:
                if col not in input_encoded.columns:
                    input_encoded[col] = 0
            
            input_encoded = input_encoded[trained_columns]
            input_scaled = scaler.transform(input_encoded)
            
            prediction = model.predict(input_scaled)[0]
            prediction = max(prediction, 0)
            
        except Exception as e:
            return f"Error in model prediction: {str(e)}"
        
        # Calculate total yield
        total_yield = prediction * area_hectares
        
        # Store prediction in database (non-critical)
        store_prediction_in_db(
            district_id, crop_id, area, area_unit, rainfall, temperature,
            soil_ph, nitrogen, phosphorus, potassium, 
            round(prediction, 2), round(total_yield, 2)
        )
        
        yield_units_per_ha = {
            'Rice': 'kg',
            'Sugar Cane': 'kg', 
'Cotton': 'kg',
            'Ground Nut': 'kg',
            'Sun Flower': 'kg'
        }
        
        base_unit = yield_units_per_ha.get(crop, 'units')
        
        if area_unit == 'acres':
            display_yield = prediction / 2.47105
            yield_unit = f'{base_unit}/acre'
        else:
            display_yield = prediction
            yield_unit = f'{base_unit}/ha'
        
        return render_template('prediction.html',
                             district=district,
                             crop=crop,
                             area=area,
                             area_unit=area_unit,
                             rainfall=rainfall,
                             temperature=temperature,
                             soil_ph=soil_ph,
                             nitrogen=nitrogen,
                             phosphorus=phosphorus,
                             potassium=potassium,
                             yield_per_ha=round(display_yield, 2),
                             total_yield=round(total_yield, 2),
                             yield_unit=yield_unit)
    
    except ValueError:
        return render_template('error.html', 
                               error="Please check your input values. All fields should contain valid numbers.")
    except Exception as e:
        return render_template('error.html', error=f"Error: {str(e)}")

@app.route('/history')
def prediction_history():
    """Show prediction history"""
    # Without database, return empty history
    return render_template('history.html', history=[])

@app.route('/chat', methods=['POST', 'GET', 'OPTIONS'])
def chat():
    """Handle AI chat requests with Gemini API"""
    try:
        if request.method == 'OPTIONS':
            response = jsonify({'status': 'ok'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
            return response
            
        if request.method == 'GET':
            return jsonify({
                'response': '🌾 Welcome to Agricultural Assistant! I\'m powered by Google Gemini AI.\n\nI can help you with:\n- Crop selection and management\n- Soil health and fertilization\n- Irrigation planning\n- Pest and disease control\n- Yield optimization\n\nPlease ask me anything about farming!'
            })
        
        data = request.get_json()
        if not data:
            return jsonify({'response': 'No data received'}), 400
            
        user_message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id', None)
        
        if not user_message:
            return jsonify({'response': 'Please provide a message.'}), 400
        
        if len(user_message) > 2000:
            return jsonify({'response': 'Message too long. Please keep it under 2000 characters.'}), 400
        
        print(f"💬 Chat request received: {user_message[:100]}...")
        
        conversation_history = get_chat_history(conversation_id, limit=5)
        ai_response = get_gemini_response(user_message, conversation_history)
        
        store_chat_history(user_message, ai_response, conversation_id)
        
        response = jsonify({
            'response': ai_response,
            'conversation_id': conversation_id,
            'model': 'Gemini Pro'
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
    except Exception as e:
        print(f"❌ Chat error: {e}")
        response = jsonify({'response': 'I apologize, but I\'m having trouble responding right now. Please try again.'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    db_status = "configured" if get_db_connection() else "not-configured"
    model_status = "loaded" if model is not None and scaler is not None else "not-loaded"
    
    return jsonify({
        'status': 'healthy',
        'service': 'Agricultural Yield Prediction',
        'deployment': 'Vercel Serverless',
        'ai_chat': 'enabled' if GEMINI_API_KEY else 'disabled',
        'database': db_status,
        'ml_model': model_status,
        'timestamp': datetime.now().isoformat()
    }), 200

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error="Internal server error"), 500

@app.after_request
def after_request(response):
    """Add CORS headers to all responses"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Vercel requires the app to be exported as 'handler' or directly as 'app'
handler = app

# For local development
if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Agricultural Yield Prediction System (Vercel Mode)")
    print("=" * 60)
    app.run(debug=True, host='127.0.0.1', port=3000)
