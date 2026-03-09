from flask import Flask, render_template, request, jsonify
import mysql.connector
import pickle
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv
import google.generativeai as genai

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    print("✅ Gemini API configured successfully!")
else:
    print("⚠️  Gemini API key not found in .env file")
    print("Please set GEMINI_API_KEY in .env file to enable Gemini chatbot")

# Load trained model and scaler
try:
    with open('models/random_forest_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('models/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    print("✅ ML models loaded successfully!")
except Exception as e:
    print(f"❌ Model loading error: {e}")
    print("Please train the model first using train_model.py")

def get_db_connection():
    """Create database connection"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='agriculture_yield'
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None

def check_database_tables():
    """Check if required tables exist and have data"""
    conn = get_db_connection()
    if conn is None:
        print("❌ Cannot connect to database for table check")
        return False
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Check yield_data table
        cursor.execute("SHOW TABLES LIKE 'yield_data'")
        yield_table_exists = cursor.fetchone() is not None
        print(f"📊 yield_data table exists: {yield_table_exists}")
        
        if yield_table_exists:
            # Check table structure
            cursor.execute("DESCRIBE yield_data")
            columns = cursor.fetchall()
            print("📋 yield_data columns:")
            for col in columns:
                print(f"  - {col['Field']} ({col['Type']})")
            
            # Check record count
            cursor.execute("SELECT COUNT(*) as count FROM yield_data")
            count = cursor.fetchone()['count']
            print(f"🔢 Total records in yield_data: {count}")
            
            # Check recent records
            cursor.execute("""
                SELECT y.id, d.district_name, c.crop_name, y.created_at 
                FROM yield_data y 
                LEFT JOIN districts d ON y.district_id = d.id 
                LEFT JOIN crops c ON y.crop_id = c.id 
                ORDER BY y.id DESC LIMIT 5
            """)
            recent = cursor.fetchall()
            print("📅 Recent records:")
            for rec in recent:
                print(f"  - ID: {rec['id']}, District: {rec['district_name']}, Crop: {rec['crop_name']}")
        
        # Check districts table
        cursor.execute("SELECT COUNT(*) as count FROM districts")
        districts_count = cursor.fetchone()['count']
        print(f"🏙️  Districts count: {districts_count}")
        
        # Check crops table
        cursor.execute("SELECT COUNT(*) as count FROM crops")
        crops_count = cursor.fetchone()['count']
        print(f"🌾 Crops count: {crops_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error checking database tables: {e}")
        conn.close()
        return False

def create_chat_history_table():
    """Create chat_history table if it doesn't exist"""
    try:
        conn = get_db_connection()
        if conn is None:
            print("❌ Cannot create chat history table - database not connected")
            return False
        
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS chat_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_message TEXT NOT NULL,
            bot_response LONGTEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            conversation_id VARCHAR(50)
        )
        """
        cursor.execute(create_table_query)
        conn.commit()
        conn.close()
        print("✅ Chat history table created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating chat history table: {e}")
        return False

def store_chat_history(user_message, bot_response, conversation_id=None):
    """Store chat messages in database"""
    try:
        conn = get_db_connection()
        if conn is None:
            print("⚠️  Cannot store chat - database not connected")
            return False
        
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO chat_history (user_message, bot_response, conversation_id)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (user_message, bot_response, conversation_id))
        conn.commit()
        conn.close()
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
        
        cursor = conn.cursor(dictionary=True)
        if conversation_id:
            query = """
            SELECT user_message, bot_response, created_at 
            FROM chat_history 
            WHERE conversation_id = %s 
            ORDER BY created_at DESC 
            LIMIT %s
            """
            cursor.execute(query, (conversation_id, limit))
        else:
            query = """
            SELECT user_message, bot_response, created_at 
            FROM chat_history 
            ORDER BY created_at DESC 
            LIMIT %s
            """
            cursor.execute(query, (limit,))
        
        history = cursor.fetchall()
        conn.close()
        return list(reversed(history))  # Return in chronological order
    except Exception as e:
        print(f"⚠️  Error retrieving chat history: {e}")
        return []

def get_gemini_response(user_message, conversation_history=None):
    """
    Get response from Google Gemini API with conversation context
    """
    try:
        if not GEMINI_API_KEY:
            return get_fallback_response(user_message)
        
        # Initialize Gemini model (using gemini-2.5-flash - latest available model)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Create system prompt for agricultural context
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
            for item in conversation_history:
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
        
        # Start conversation with system prompt
        chat = model.start_chat(history=[])
        
        # Send system prompt first
        response = chat.send_message(system_prompt)
        
        # Then send conversation history and current message
        full_message = ""
        if conversation_history:
            for item in conversation_history[-3:]:  # Keep last 3 exchanges for context
                full_message += f"User: {item.get('user_message', '')}\nAssistant: {item.get('bot_response', '')}\n\n"
        
        full_message += f"User: {user_message}"
        
        response = chat.send_message(full_message)
        ai_response = response.text
        
        print(f"✅ Gemini API response received: {len(ai_response)} characters")
        return ai_response
        
    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        return get_fallback_response(user_message)

def store_prediction_in_db(district_id, crop_id, area, area_unit, rainfall, temperature,
                          soil_ph, nitrogen, phosphorus, potassium, yield_per_ha, total_yield):
    """Store the prediction in database for historical records"""
    try:
        conn = get_db_connection()
        if conn is None:
            print("❌ Database connection failed in store_prediction_in_db")
            return False
            
        cursor = conn.cursor()
        
        current_year = datetime.now().year
        
        # First, let's ensure the table has the created_at column
        try:
            cursor.execute("ALTER TABLE yield_data ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            conn.commit()
            print("✅ Ensured created_at column exists")
        except Exception as e:
            print(f"ℹ️  created_at column check: {e}")
        
        insert_query = """
        INSERT INTO yield_data 
        (district_id, crop_id, year, area, area_unit, rainfall, temperature, 
         soil_ph, nitrogen, phosphorus, potassium, yield_per_ha, total_yield, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        
        print(f"💾 Storing prediction: District={district_id}, Crop={crop_id}, Area={area} {area_unit}")
        
        cursor.execute(insert_query, (
            district_id, crop_id, current_year, area, area_unit, rainfall, temperature,
            soil_ph, nitrogen, phosphorus, potassium, yield_per_ha, total_yield
        ))
        
        conn.commit()
        
        # Get the inserted ID to verify
        cursor.execute("SELECT LAST_INSERT_ID() as id")
        inserted_id = cursor.fetchone()[0]
        
        # Verify the record was inserted
        cursor.execute("SELECT * FROM yield_data WHERE id = %s", (inserted_id,))
        inserted_record = cursor.fetchone()
        
        conn.close()
        
        if inserted_record:
            print(f"✅ Prediction stored in database successfully! ID: {inserted_id}")
            return True
        else:
            print(f"❌ Prediction storage verification failed for ID: {inserted_id}")
            return False
        
    except Exception as e:
        print(f"❌ Error storing prediction: {e}")
        return False

def get_deepseek_response(user_message):
    """
    Get response from DeepSeek AI API with better error handling
    """
    try:
        API_KEY = "sk-b41c1e48b4d64aa9848ee65f9cdca766"
        API_URL = "https://api.deepseek.com/v1/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        # Enhanced system prompt for better agricultural responses
        system_prompt = """You are an agricultural expert specializing in Tamil Nadu farming practices. 
        Provide detailed, practical advice about:
        - Crop selection for different Tamil Nadu districts
        - Soil management and fertilization
        - Irrigation and water management
        - Pest and disease control
        - Yield optimization techniques
        - Climate-resilient farming practices
        - Organic farming methods
        - Government schemes for farmers in Tamil Nadu
        
        Always be specific to Tamil Nadu conditions and provide actionable recommendations.
        Use metric units and local terminology familiar to Tamil Nadu farmers.
        Be concise but informative in your responses. Keep responses under 500 words.
        If you don't know something, admit it and suggest consulting local agricultural officers."""
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7,
            "max_tokens": 800,
            "stream": False
        }
        
        print(f"🤖 Sending request to DeepSeek API: {user_message[:100]}...")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        # Check for API errors
        if response.status_code != 200:
            print(f"❌ DeepSeek API error: {response.status_code} - {response.text}")
            return get_fallback_response(user_message)
        
        response.raise_for_status()
        result = response.json()
        
        # Check if response contains the expected data
        if 'choices' in result and len(result['choices']) > 0:
            ai_response = result['choices'][0]['message']['content']
            print(f"✅ DeepSeek API response received: {len(ai_response)} characters")
            return ai_response
        else:
            print(f"❌ Unexpected API response format: {result}")
            return get_fallback_response(user_message)
        
    except requests.exceptions.Timeout:
        print("❌ DeepSeek API timeout")
        return "I apologize for the delay. The agricultural knowledge base is taking longer than expected to respond. Please try your question again in a moment."
    
    except requests.exceptions.RequestException as e:
        print(f"❌ DeepSeek API request failed: {e}")
        return get_fallback_response(user_message)
    
    except Exception as e:
        print(f"❌ DeepSeek API unexpected error: {e}")
        return get_fallback_response(user_message)

def get_fallback_response(user_message):
    """Fallback responses if DeepSeek API fails"""
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

        "banana cultivation": """🍌 **Banana Cultivation Guide for Tamil Nadu:**

**Popular Varieties:**
• Grand Naine (most popular)
• Robusta
• Nendran (traditional)

**Planting Details:**
• Spacing: 1.8m x 1.8m
• Density: 3000 plants/hectare

**Fertilizer Requirements:**
• N: 200g/plant, P: 60g/plant, K: 300g/plant
• Apply in 6-7 splits
• FYM: 10kg/plant

**Irrigation:**
• Daily drip irrigation preferred
• Critical stages: vegetative, flowering, bunch development""",

        "general advice": """🤖 **Agricultural Assistant for Tamil Nadu**

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
• Government schemes information
• Market trends

Please ask specific questions about your farming needs! 🚜"""
    }
    
    user_lower = user_message.lower()
    
    # Check for keywords in user message
    if any(keyword in user_lower for keyword in ['rainfall', 'low rain', 'dry area', 'drought', 'water scarce']):
        return agricultural_knowledge["best crops for low rainfall"]
    elif any(keyword in user_lower for keyword in ['soil', 'fertility', 'rice', 'paddy']):
        return agricultural_knowledge["improve soil fertility for rice"]
    elif any(keyword in user_lower for keyword in ['fertilizer', 'sugarcane', 'sugar cane']):
        return agricultural_knowledge["fertilizer for sugarcane"]
    elif any(keyword in user_lower for keyword in ['banana', 'plantain']):
        return agricultural_knowledge["banana cultivation"]
    elif any(keyword in user_lower for keyword in ['hello', 'hi', 'hey', 'help']):
        return agricultural_knowledge["general advice"]
    else:
        return agricultural_knowledge["general advice"]

@app.route('/')
def index():
    """Main page with prediction form"""
    # Check database status on home page load
    print("\n" + "="*50)
    print("🏠 Home page loaded - Checking database...")
    check_database_tables()
    print("="*50 + "\n")
    
    conn = get_db_connection()
    if conn is None:
        return "Database connection failed. Please check your database setup."
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get districts and crops for dropdown
        cursor.execute("SELECT * FROM districts ORDER BY district_name")
        districts = cursor.fetchall()
        
        cursor.execute("SELECT * FROM crops ORDER BY crop_name")
        crops = cursor.fetchall()
        
        conn.close()
        
        return render_template('index.html', districts=districts, crops=crops)
    
    except Exception as e:
        conn.close()
        return f"Error loading page: {str(e)}"

@app.route('/predict', methods=['POST'])
def predict():
    """Handle yield prediction requests"""
    try:
        # Get form data
        district_id = int(request.form['district'])
        crop_id = int(request.form['crop'])
        area = float(request.form['area'])
        area_unit = request.form['area_unit']
        rainfall = float(request.form['rainfall'])
        temperature = float(request.form['temperature'])
        soil_ph = float(request.form['soil_ph'])
        nitrogen = float(request.form['nitrogen'])
        phosphorus = float(request.form['phosphorus'])
        potassium = float(request.form['potassium'])
        
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
        conn = get_db_connection()
        if conn is None:
            return "Database connection failed"
            
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT district_name FROM districts WHERE id = %s", (district_id,))
        district_result = cursor.fetchone()
        if not district_result:
            conn.close()
            return "Error: District not found"
        district = district_result['district_name']
        
        cursor.execute("SELECT crop_name FROM crops WHERE id = %s", (crop_id,))
        crop_result = cursor.fetchone()
        if not crop_result:
            conn.close()
            return "Error: Crop not found"
        crop = crop_result['crop_name']
        
        conn.close()
        
        # Prepare input data for ML model
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
        
        # Convert to DataFrame and create dummy variables
        input_df = pd.DataFrame([input_data])
        input_encoded = pd.get_dummies(input_df)
        
        # Ensure all columns from training are present
        try:
            trained_columns = scaler.feature_names_in_
            for col in trained_columns:
                if col not in input_encoded.columns:
                    input_encoded[col] = 0
            
            input_encoded = input_encoded[trained_columns]
            
            # Scale input
            input_scaled = scaler.transform(input_encoded)
            
            # Make prediction (yield per hectare)
            prediction = model.predict(input_scaled)[0]
            
            # Ensure prediction is reasonable
            prediction = max(prediction, 0)  # No negative yields
            
        except Exception as e:
            return f"Error in model prediction: {str(e)}"
        
        # Calculate total yield
        total_yield = prediction * area_hectares
        
        # Store prediction in database
        storage_success = store_prediction_in_db(
            district_id, crop_id, area, area_unit, rainfall, temperature,
            soil_ph, nitrogen, phosphorus, potassium, 
            round(prediction, 2), round(total_yield, 2)
        )
        
        if not storage_success:
            print("⚠️  Prediction made but storage failed - continuing to show results")
        
        # Determine yield unit based on crop and selected area unit
        yield_units_per_ha = {
            'Rice': 'kg',
            'Sugar Cane': 'kg', 
            'Banana': 'bunches',
            'Ground Nut': 'kg',
            'Cotton': 'kg',
            'Sun Flower': 'kg'
        }
        
        base_unit = yield_units_per_ha.get(crop, 'units')
        
        # Adjust yield display based on area unit selected
        if area_unit == 'acres':
            # Convert yield from per hectare to per acre
            display_yield = prediction / 2.47105  # 1 hectare = 2.47105 acres
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
    
    except ValueError as e:
        return f"Error: Please check your input values. All fields should contain valid numbers."
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/history')
def prediction_history():
    """Show prediction history"""
    print("\n" + "="*50)
    print("📊 History page loaded - Fetching predictions...")
    
    conn = get_db_connection()
    if conn is None:
        print("❌ Database connection failed in prediction_history")
        return render_template('history.html', history=[])
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # First, let's check if the table has any data
        cursor.execute("SELECT COUNT(*) as count FROM yield_data")
        total_count = cursor.fetchone()['count']
        print(f"📊 Total records in yield_data: {total_count}")
        
        if total_count == 0:
            print("ℹ️  No records found in yield_data table")
            conn.close()
            return render_template('history.html', history=[])
        
        # Get recent prediction history (last 20 records)
        cursor.execute("""
            SELECT d.district_name, c.crop_name, y.area, y.area_unit, 
                   y.yield_per_ha, y.total_yield, y.created_at
            FROM yield_data y
            JOIN districts d ON y.district_id = d.id
            JOIN crops c ON y.crop_id = c.id
            ORDER BY y.created_at DESC
            LIMIT 20
        """)
        
        history = cursor.fetchall()
        print(f"📋 History records fetched: {len(history)}")
        
        # Debug: Print what we got
        for i, record in enumerate(history):
            print(f"Record {i+1}: {record['district_name']} - {record['crop_name']} - {record['yield_per_ha']}")
        
        conn.close()
        
        return render_template('history.html', history=history)
    
    except Exception as e:
        conn.close()
        print(f"❌ Error loading history: {e}")
        return render_template('history.html', history=[])

@app.route('/chat', methods=['POST', 'GET', 'OPTIONS'])
def chat():
    """Handle AI chat requests with Gemini API and conversation history"""
    try:
        # Handle preflight OPTIONS request
        if request.method == 'OPTIONS':
            response = jsonify({'status': 'ok'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
            return response
            
        # Handle GET request (when page loads with /chat in URL)
        if request.method == 'GET':
            return jsonify({
                'response': '🌾 Welcome to Agricultural Assistant! I\'m powered by Google Gemini AI.\n\nI can help you with:\n- Crop selection and management\n- Soil health and fertilization\n- Irrigation planning\n- Pest and disease control\n- Yield optimization\n- Government farming schemes\n- Organic farming practices\n\nPlease ask me anything about farming in Tamil Nadu!'
            })
        
        # Handle POST request (normal chat)
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
        print(f"📌 Conversation ID: {conversation_id}")
        
        # Get conversation history for context
        conversation_history = get_chat_history(conversation_id, limit=5)
        
        # Get Gemini response
        ai_response = get_gemini_response(user_message, conversation_history)
        
        # Store in database
        store_chat_history(user_message, ai_response, conversation_id)
        
        print(f"🤖 Response generated: {len(ai_response)} characters")
        
        response = jsonify({
            'response': ai_response,
            'conversation_id': conversation_id,
            'model': 'Gemini Pro'
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
    except Exception as e:
        print(f"❌ Chat error: {e}")
        error_response = "I apologize, but I'm having trouble responding right now. Please try again in a moment."
        response = jsonify({'response': error_response})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/chat/', methods=['POST', 'GET', 'OPTIONS'])
def chat_with_slash():
    """Handle /chat/ with trailing slash"""
    return chat()

@app.route('/chat-history', methods=['GET'])
def get_chat_history_route():
    """Retrieve chat history for a conversation"""
    try:
        conversation_id = request.args.get('conversation_id', None)
        limit = request.args.get('limit', 20, type=int)
        
        history = get_chat_history(conversation_id, limit)
        
        response = jsonify({
            'history': history,
            'conversation_id': conversation_id,
            'count': len(history)
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
    except Exception as e:
        print(f"❌ Error retrieving chat history: {e}")
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    db_status = "connected" if get_db_connection() else "disconnected"
    model_status = "loaded" if 'model' in globals() else "not loaded"
    
    return jsonify({
        'status': 'healthy',
        'service': 'Agricultural Yield Prediction',
        'ai_chat': 'enabled',
        'database': db_status,
        'ml_model': model_status,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/debug-db')
def debug_database():
    """Debug endpoint to check database status"""
    print("\n" + "="*50)
    print("🐛 Database Debug Information")
    print("="*50)
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'})
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Check all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_info = {}
        
        for table in tables:
            table_name = list(table.values())[0]
            cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            count = cursor.fetchone()['count']
            table_info[table_name] = count
        
        # Check yield_data structure and sample data
        cursor.execute("DESCRIBE yield_data")
        yield_columns = [col['Field'] for col in cursor.fetchall()]
        
        cursor.execute("SELECT * FROM yield_data ORDER BY id DESC LIMIT 3")
        sample_data = cursor.fetchall()
        
        conn.close()
        
        return jsonify({
            'tables': table_info,
            'yield_data_columns': yield_columns,
            'sample_data': sample_data
        })
        
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

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

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Starting Agricultural Yield Prediction System...")
    print("🌾 Available at: http://localhost:5000")
    print("🤖 AI Chat Assistant: ENABLED (Google Gemini)")
    print("🔑 Gemini API: CONFIGURED" if GEMINI_API_KEY else "⚠️  Gemini API: NOT CONFIGURED")
    print("📊 ML Model: LOADED")
    print("💾 Database: READY")
    print("📈 History Page: ENABLED")
    print("💬 Chat History: ENABLED")
    print("🐛 Debug Features: ENABLED")
    print("🔧 CORS: ENABLED")
    print("=" * 60)
    print("📋 Available Routes:")
    print("   • Main App: http://localhost:5000")
    print("   • Health Check: http://localhost:5000/health")
    print("   • Prediction History: http://localhost:5000/history")
    print("   • Chat API: http://localhost:5000/chat")
    print("   • Chat History: http://localhost:5000/chat-history")
    print("   • Database Debug: http://localhost:5000/debug-db")
    print("=" * 60)
    
    # Initial database setup
    print("\n🔍 Performing initial database setup...")
    check_database_tables()
    create_chat_history_table()
    print("✅ System initialization complete!\n")
    
    app.run(debug=True, host='localhost', port=5000)