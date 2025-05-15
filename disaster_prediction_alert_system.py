
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import sqlite3
import random
import time

# -------------------------------------
# 1. Train AI Model
# -------------------------------------
print("⚙️ Training AI disaster prediction model...")

# Sample dataset
data = {
    'temperature': [30, 45, 25, 40, 20, 35, 50],
    'humidity': [70, 20, 90, 30, 95, 50, 10],
    'wind_speed': [20, 60, 15, 50, 10, 40, 70],
    'disaster': ['No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes']
}

df = pd.DataFrame(data)
x = df[['temperature', 'humidity', 'wind_speed']]
y = df['disaster']

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
model = RandomForestClassifier()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model trained with accuracy: {accuracy:.2f}")

# -------------------------------------
# 2. Set up database
# -------------------------------------
print("🧱 Setting up SQLite database...")
conn = sqlite3.connect('disaster_alerts.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY,
    disaster_type TEXT,
    location TEXT,
    timestamp TEXT
)
''')
conn.commit()

# -------------------------------------
# 3. Simulate real-time data + predict + log alert
# -------------------------------------
locations = ['Mumbai', 'Chennai', 'Delhi', 'Kolkata']
print("🌐 Starting real-time disaster monitoring...")

for i in range(5):  # simulate 5 data points
    # Simulate incoming data
    temp = random.randint(20, 50)
    hum = random.randint(10, 100)
    wind = random.randint(10, 80)
    loc = random.choice(locations)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    # Make prediction
    pred = model.predict([[temp, hum, wind]])[0]

    # Print result
    print(f"\nData Received: {temp}°C, {hum}% humidity, {wind} km/h wind, {loc}")
    print(f"Prediction: {'⚠️ Disaster' if pred == 'Yes' else '✅ No disaster'}")

    # If disaster, insert alert into database
    if pred == 'Yes':
        cursor.execute('''
            INSERT INTO alerts (disaster_type, location, timestamp)
            VALUES (?, ?, ?)
        ''', ('Generic Disaster', loc, timestamp))
        conn.commit()
        print(f"🚨 Alert logged to database for {loc} at {timestamp}")

    time.sleep(1)  # wait before next reading

# -------------------------------------
# 4. Show saved alerts
# -------------------------------------
print("\n📋 Saved disaster alerts:")
cursor.execute('SELECT * FROM alerts')
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
print("✅ Monitoring complete.")
