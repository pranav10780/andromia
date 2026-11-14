from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('local_health.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS health_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            systolic_bp INTEGER,
            diastolic_bp INTEGER,
            effective_dose INTEGER,
            sleep_hours REAL,
            mood_score INTEGER
        );
    ''')
    conn.commit()
    conn.close()

init_db()

#api
@app.route('/api/log', methods=['POST'])
def log_health_data():
    data = request.get_json()
    
    systolic = data.get('systolic_bp')
    diastolic = data.get('diastolic_bp')
    sleep = data.get('sleep_hours')
    mood = data.get('mood_score')

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO health_logs (systolic_bp, diastolic_bp, sleep_hours, mood_score) VALUES (?, ?, ?, ?)',
        (systolic, diastolic, sleep, mood)
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Health data logged successfully"}), 201

@app.route('/api/health/latest', methods=['GET'])
def get_latest_health():
    conn = get_db_connection()
    result = conn.execute(
        'SELECT * FROM health_logs ORDER BY id DESC LIMIT 1'
    )
    row = result.fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "No data found"}), 404
        
    metrics = {
        "systolic_bp": row['systolic_bp'],
        "diastolic_bp": row['diastolic_bp'],
        "sleep_hours": row['sleep_hours'],
        "mood_score": row['mood_score']
    }

    alert=""
    #diagnostics
    if metrics["systolic_bp"] > 130:
        alert = "Elevated blood pressure detected. Drink 500ml water."
    elif metrics["sleep_hours"] < 6:
        alert = "Sleep deficit. Engage red-shift cabin lighting."
    
    return jsonify({
        "metrics": metrics,
        "alert": alert
    })


#front end
@app.route('/')
def serve_frontend():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(port=8080, debug=True)
