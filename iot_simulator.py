import time 
import json 
import random 
import request
from datetime import datetime

# --- CONFIGURATION ---
# This is where your FastAPI backend will eventually live. 
# We use localhost for local testing.
ENDPOINT_URL = "http://localhost:8000/api/telemetry" 
INTERVAL_SECONDS = 2 

def generate_motor_data():
    """Generates synthetic temperature and vibration data for a heavy-duty motor."""
    
    # 1. The 95% / 5% Split Logic
    # random.random() generates a float between 0.0 and 1.0. 
    # If it's less than 0.05, we trigger an anomaly.
    is_anomaly = random.random() < 0.05 
    
    if not is_anomaly:
        # NORMAL STATE (95% of the time)
        # Motor operates within safe parameters
        temperature = round(random.uniform(60.0, 75.0), 2)  # Normal temp: 60-75°C
        vibration = round(random.uniform(10.0, 15.0), 2)    # Normal vibration: 10-15 mm/s
        data_label = "NORMAL" # Internal label for terminal output
    else:
        # ANOMALY STATE (5% of the time)
        # Injects a sudden spike simulating a failing bearing or overheating
        temperature = round(random.uniform(85.0, 110.0), 2) # Overheating
        vibration = round(random.uniform(25.0, 40.0), 2)    # Severe vibration
        data_label = "ANOMALY (SPIKE)"

    # 2. Construct the JSON Payload
    payload = {
        "sensor_id": "heavy_motor_alpha_01",
        "timestamp": datetime.utcnow().isoformat() + "Z", # Standard ISO 8601 time format
        "metrics": {
            "temperature_celsius": temperature,
            "vibration_mms": vibration
        }
    }
    
    return payload, data_label

def start_stream():
    """Runs the continuous loop to stream data."""
    print("🚀 Starting Heavy-Duty Motor IoT Simulator...")
    print(f"📡 Target Endpoint: {ENDPOINT_URL}")
    print(f"⏱️  Interval: Every {INTERVAL_SECONDS} seconds\n")
    print("-" * 50)

    while True:
        # Generate the data payload
        payload, data_label = generate_motor_data()
        
        try:
            # 3. The Stream (HTTP POST)
            # In a real environment, this sends the data to your FastAPI server.
            response = requests.post(ENDPOINT_URL, json=payload, timeout=2)
            
            # For testing right now, we will just print it to the console
            # Once your FastAPI backend is ready, uncomment the line above!
            print(f"[{data_label}] Data Generated: {json.dumps(payload)}")
            
        except requests.exceptions.RequestException as e:
            # If the backend is down, it won't crash the sensor, it just logs the error
            print(f"⚠️ Connection Error: Could not reach {ENDPOINT_URL} - {e}")
            
        # Wait 2 seconds before sending the next reading
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    try:
        start_stream()
    except KeyboardInterrupt:
        print("\n🛑 Simulator stopped by user.")
