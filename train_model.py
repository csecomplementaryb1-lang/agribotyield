import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
import pickle
import mysql.connector
import os

def create_database_connection():
    """Create database connection"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Default XAMPP password is empty
            database='agriculture_yield'
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None

def create_tables():
    """Create necessary tables if they don't exist"""
    conn = create_database_connection()
    if conn is None:
        return False
    
    cursor = conn.cursor()
    
    try:
        # Create districts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS districts (
                id INT PRIMARY KEY AUTO_INCREMENT,
                district_name VARCHAR(100) NOT NULL
            )
        """)
        
        # Create crops table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS crops (
                id INT PRIMARY KEY AUTO_INCREMENT,
                crop_name VARCHAR(100) NOT NULL
            )
        """)
        
        # Create yield_data table (UPDATED with area fields)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS yield_data (
                id INT PRIMARY KEY AUTO_INCREMENT,
                district_id INT,
                crop_id INT,
                year INT,
                area FLOAT,
                area_unit VARCHAR(10),
                rainfall FLOAT,
                temperature FLOAT,
                soil_ph FLOAT,
                nitrogen FLOAT,
                phosphorus FLOAT,
                potassium FLOAT,
                yield_per_ha FLOAT,
                total_yield FLOAT,
                FOREIGN KEY (district_id) REFERENCES districts(id),
                FOREIGN KEY (crop_id) REFERENCES crops(id)
            )
        """)
        
        conn.commit()
        print("Tables created successfully!")
        return True
        
    except mysql.connector.Error as e:
        print(f"Error creating tables: {e}")
        return False
    finally:
        conn.close()

def insert_sample_data():
    """Insert sample districts and crops data"""
    conn = create_database_connection()
    if conn is None:
        return False
    
    cursor = conn.cursor()
    
    try:
        # Check if districts already exist
        cursor.execute("SELECT COUNT(*) FROM districts")
        if cursor.fetchone()[0] == 0:
            # Insert Tamil Nadu districts
            districts = [
                'Ariyalur', 'Chennai', 'Coimbatore', 'Cuddalore', 'Dharmapuri',
                'Dindigul', 'Erode', 'Kanchipuram', 'Kanyakumari', 'Karur',
                'Krishnagiri', 'Madurai', 'Nagapattinam', 'Namakkal', 'Nilgiris',
                'Perambalur', 'Pudukkottai', 'Ramanathapuram', 'Salem', 'Sivaganga',
                'Thanjavur', 'Theni', 'Thoothukudi', 'Tiruchirappalli', 'Tirunelveli',
                'Tiruppur', 'Tiruvallur', 'Tiruvannamalai', 'Tiruvarur', 'Vellore',
                'Viluppuram', 'Virudhunagar'
            ]
            
            for district in districts:
                cursor.execute("INSERT INTO districts (district_name) VALUES (%s)", (district,))
        
        # Check if crops already exist
        cursor.execute("SELECT COUNT(*) FROM crops")
        if cursor.fetchone()[0] == 0:
            crops = ['Rice', 'Sugar Cane', 'Banana', 'Ground Nut', 'Cotton', 'Sun Flower']
            
            for crop in crops:
                cursor.execute("INSERT INTO crops (crop_name) VALUES (%s)", (crop,))
        
        conn.commit()
        print("Sample data inserted successfully!")
        return True
        
    except mysql.connector.Error as e:
        print(f"Error inserting sample data: {e}")
        return False
    finally:
        conn.close()

def generate_training_data():
    """Generate sample training data with area information"""
    conn = create_database_connection()
    if conn is None:
        return False
    
    cursor = conn.cursor()
    
    try:
        # Clear existing training data
        cursor.execute("DELETE FROM yield_data")
        
        # Get all districts and crops
        cursor.execute("SELECT id FROM districts")
        districts = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id FROM crops")
        crops = [row[0] for row in cursor.fetchall()]
        
        sample_data = []
        
        for year in range(2015, 2024):
            for district in districts:
                for crop in crops:
                    # Generate area data (1-50 hectares/acres)
                    area = np.random.uniform(1, 50)
                    area_unit = np.random.choice(['acres', 'hectares'])
                    
                    # Generate realistic values based on crop and district
                    base_yield_per_ha = {
                        1: 2500,  # Rice (kg/ha)
                        2: 70000, # Sugar Cane (kg/acre) - but we'll convert to per hectare
                        3: 35000, # Banana (bunches/acre) - but we'll convert to per hectare
                        4: 1500,  # Ground Nut (kg/ha)
                        5: 500,   # Cotton (kg/ha)
                        6: 800    # Sun Flower (kg/ha)
                    }
                    
                    # Convert all yields to per hectare for consistent training
                    conversion_factors = {
                        1: 1.0,    # Rice already in kg/ha
                        2: 0.4047, # Sugar Cane: kg/acre to kg/ha (1 acre = 0.4047 ha)
                        3: 0.4047, # Banana: bunches/acre to bunches/ha
                        4: 1.0,    # Ground Nut already in kg/ha
                        5: 1.0,    # Cotton already in kg/ha
                        6: 1.0     # Sun Flower already in kg/ha
                    }
                    
                    base_yield = base_yield_per_ha[crop] * conversion_factors[crop]
                    
                    rainfall = np.random.normal(900, 200)
                    temperature = np.random.normal(28, 3)
                    soil_ph = np.random.normal(6.5, 0.5)
                    nitrogen = np.random.normal(250, 50)
                    phosphorus = np.random.normal(50, 10)
                    potassium = np.random.normal(200, 40)
                    
                    # Calculate yield_per_ha with some randomness
                    yield_per_ha = base_yield + (
                        (rainfall - 900) * 0.1 +
                        (temperature - 28) * 10 +
                        (soil_ph - 6.5) * 100 +
                        (nitrogen - 250) * 0.5 +
                        (phosphorus - 50) * 1 +
                        (potassium - 200) * 0.3 +
                        np.random.normal(0, base_yield * 0.1)
                    )
                    
                    # Ensure yield is positive
                    yield_per_ha = max(yield_per_ha, 0)
                    
                    # Convert area to hectares for total yield calculation
                    if area_unit == 'acres':
                        area_hectares = area * 0.404686
                    else:
                        area_hectares = area
                    
                    # Calculate total yield
                    total_yield = yield_per_ha * area_hectares
                    
                    sample_data.append((
                        district, crop, year, area, area_unit, rainfall, temperature,
                        soil_ph, nitrogen, phosphorus, potassium, yield_per_ha, total_yield
                    ))
        
        # Insert sample data
        insert_query = """
        INSERT INTO yield_data 
        (district_id, crop_id, year, area, area_unit, rainfall, temperature, 
         soil_ph, nitrogen, phosphorus, potassium, yield_per_ha, total_yield)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.executemany(insert_query, sample_data)
        conn.commit()
        print(f"Generated {len(sample_data)} training records with area data!")
        return True
        
    except mysql.connector.Error as e:
        print(f"Error generating training data: {e}")
        return False
    finally:
        conn.close()

def train_model():
    """Train the Random Forest model to predict yield PER HECTARE"""
    conn = create_database_connection()
    if conn is None:
        return False
    
    try:
        # Load data - we're predicting yield_per_ha (not total_yield)
        query = """
        SELECT d.district_name, c.crop_name, y.rainfall, y.temperature, 
               y.soil_ph, y.nitrogen, y.phosphorus, y.potassium, y.yield_per_ha
        FROM yield_data y
        JOIN districts d ON y.district_id = d.id
        JOIN crops c ON y.crop_id = c.id
        """
        
        df = pd.read_sql(query, conn)
        
        if len(df) == 0:
            print("No data found for training!")
            return False
        
        print(f"Training on {len(df)} records...")
        print(f"Yield range: {df['yield_per_ha'].min():.2f} to {df['yield_per_ha'].max():.2f}")
        
        # Preprocessing
        X = pd.get_dummies(df[['district_name', 'crop_name', 'rainfall', 'temperature', 
                              'soil_ph', 'nitrogen', 'phosphorus', 'potassium']])
        y = df['yield_per_ha']  # Predicting yield per hectare
        
        print(f"Features shape: {X.shape}")
        print(f"Target shape: {y.shape}")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test_scaled)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"\nModel Performance:")
        print(f"MAE: {mae:.2f} units")
        print(f"R² Score: {r2:.4f}")
        print(f"Average Yield: {y.mean():.2f}")
        print(f"MAE as % of average: {(mae/y.mean())*100:.2f}%")
        
        # Create models directory if it doesn't exist
        os.makedirs('models', exist_ok=True)
        
        # Save model and scaler
        with open('models/random_forest_model.pkl', 'wb') as f:
            pickle.dump(model, f)
        
        with open('models/scaler.pkl', 'wb') as f:
            pickle.dump(scaler, f)
        
        # Save feature names for reference
        with open('models/feature_names.pkl', 'wb') as f:
            pickle.dump(X.columns.tolist(), f)
        
        print("\nModel trained and saved successfully!")
        print(f"Model predicts: Yield per Hectare")
        return True
        
    except Exception as e:
        print(f"Error training model: {e}")
        return False
    finally:
        conn.close()

def store_prediction_data():
    """Store sample prediction data for the web interface"""
    conn = create_database_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Clear previous prediction samples
        cursor.execute("DELETE FROM yield_data WHERE year = 2024")
        
        # Add some realistic prediction samples
        prediction_samples = [
            # Rice - Thanjavur
            (get_district_id('Thanjavur'), get_crop_id('Rice'), 2024, 2.0, 'hectares', 
             950, 28.5, 6.8, 280, 60, 220, 3200, 6400),
            
            # Sugar Cane - Coimbatore  
            (get_district_id('Coimbatore'), get_crop_id('Sugar Cane'), 2024, 5.0, 'acres',
             700, 30.0, 7.2, 350, 80, 280, 28328, 57300),
            
            # Banana - Tiruchirappalli
            (get_district_id('Tiruchirappalli'), get_crop_id('Banana'), 2024, 3.0, 'hectares',
             900, 29.0, 7.5, 400, 100, 350, 14164, 42492),
        ]
        
        insert_query = """
        INSERT INTO yield_data 
        (district_id, crop_id, year, area, area_unit, rainfall, temperature, 
         soil_ph, nitrogen, phosphorus, potassium, yield_per_ha, total_yield)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.executemany(insert_query, prediction_samples)
        conn.commit()
        print("Sample prediction data stored successfully!")
        return True
        
    except Exception as e:
        print(f"Error storing prediction data: {e}")
        return False
    finally:
        conn.close()

def get_district_id(district_name):
    """Helper function to get district ID"""
    conn = create_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM districts WHERE district_name = %s", (district_name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_crop_id(crop_name):
    """Helper function to get crop ID"""
    conn = create_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM crops WHERE crop_name = %s", (crop_name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

if __name__ == "__main__":
    print("Starting agricultural yield prediction setup...")
    
    # Step 1: Create tables
    print("1. Creating tables...")
    if not create_tables():
        print("Failed to create tables!")
        exit(1)
    
    # Step 2: Insert sample data
    print("2. Inserting sample data...")
    if not insert_sample_data():
        print("Failed to insert sample data!")
        exit(1)
    
    # Step 3: Generate training data
    print("3. Generating training data...")
    if not generate_training_data():
        print("Failed to generate training data!")
        exit(1)
    
    # Step 4: Train model
    print("4. Training model...")
    if not train_model():
        print("Failed to train model!")
        exit(1)
    
    # Step 5: Store sample prediction data
    print("5. Storing sample prediction data...")
    store_prediction_data()
    
    print("\n✅ Setup completed successfully!")
    print("🎯 Model predicts: Yield per Hectare")
    print("📊 Area is used to calculate: Total Yield = Yield_per_ha × Area_in_hectares")
    print("🚀 Run: python app.py to start the web application")