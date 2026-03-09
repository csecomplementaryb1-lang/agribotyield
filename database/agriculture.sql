-- Create database
CREATE DATABASE IF NOT EXISTS agriculture_yield;

-- Use the database
USE agriculture_yield;

-- Districts of Tamil Nadu
CREATE TABLE districts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    district_name VARCHAR(100) NOT NULL
);

-- Crops table
CREATE TABLE crops (
    id INT PRIMARY KEY AUTO_INCREMENT,
    crop_name VARCHAR(100) NOT NULL
);

-- Historical yield data (UPDATED with area fields)
CREATE TABLE yield_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    district_id INT,
    crop_id INT,
    year INT,
    area FLOAT,                    -- NEW: Cultivation area
    area_unit VARCHAR(10),         -- NEW: acres or hectares
    rainfall FLOAT,
    temperature FLOAT,
    soil_ph FLOAT,
    nitrogen FLOAT,
    phosphorus FLOAT,
    potassium FLOAT,
    yield_per_ha FLOAT,            -- Yield per hectare (what model predicts)
    total_yield FLOAT,             -- Total yield (area × yield_per_ha)
    FOREIGN KEY (district_id) REFERENCES districts(id),
    FOREIGN KEY (crop_id) REFERENCES crops(id)
);

-- Insert Tamil Nadu districts
INSERT INTO districts (district_name) VALUES
('Ariyalur'),('Chennai'),('Coimbatore'),('Cuddalore'),('Dharmapuri'),
('Dindigul'),('Erode'),('Kanchipuram'),('Kanyakumari'),('Karur'),
('Krishnagiri'),('Madurai'),('Nagapattinam'),('Namakkal'),('Nilgiris'),
('Perambalur'),('Pudukkottai'),('Ramanathapuram'),('Salem'),('Sivaganga'),
('Thanjavur'),('Theni'),('Thoothukudi'),('Tiruchirappalli'),('Tirunelveli'),
('Tiruppur'),('Tiruvallur'),('Tiruvannamalai'),('Tiruvarur'),('Vellore'),
('Viluppuram'),('Virudhunagar');

-- Insert crops
INSERT INTO crops (crop_name) VALUES
('Rice'),('Sugar Cane'),('Banana'),('Ground Nut'),('Cotton'),('Sun Flower');