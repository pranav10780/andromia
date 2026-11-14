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
            effective_dose REAL,
            ucla_1 INTEGER,
            ucla_2 INTEGER,
            ucla_3 INTEGER,
            t_score REAL,
            sleep_hours REAL
        );
    ''')
    conn.commit()
    conn.close()

init_db()

#api
@app.route('/api/log', methods=['POST'])
def log_health_data():
    data = request.get_json()
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO health_logs (
            systolic_bp, diastolic_bp, effective_dose, 
            ucla_1, ucla_2, ucla_3, t_score, sleep_hours
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
        data.get('systolic_bp'),
        data.get('diastolic_bp'),
        data.get('effective_dose'),
        data.get('ucla_1'),
        data.get('ucla_2'),
        data.get('ucla_3'),
        data.get('t_score'),
        data.get('sleep_hours')
    ))
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
        "effective_dose": row['effective_dose'],
        "ucla_1": row['ucla_1'],
        "ucla_2": row['ucla_2'],
        "ucla_3": row['ucla_3'],
        "t_score": row['t_score'],
        "sleep_hours": row['sleep_hours']
    }
    ucla_total = metrics['ucla_1'] + metrics['ucla_2'] + metrics['ucla_3']

    alerts=[]
    #diagnostics
    if metrics["systolic_bp"] > 130 or metrics["diastolic_bp"] > 85:
        alerts.append("Elevated blood pressure. Hydrate and run cabin environmental checks.")
    if metrics["sleep_hours"] < 6:
        alerts.append("Sleep deficit. Engage red-shift cabin lighting 2 hours prior to sleep cycle.")
    if ucla_total >= 6: 
        alerts.append("Elevated isolation detected. Schedule a real-time comms link with Earth or engage in crew recreation.")
    if metrics["t_score"] <= -1.0:
        alerts.append("Bone mass degradation detected. Increase resistance training by 20 minutes daily.")
    if metrics["effective_dose"] > 50:
        alerts.append("High radiation dose. Verify solar flare activity and retreat to shielded quarters.")

    return jsonify({
        "metrics": metrics,
        "ucla_total": ucla_total,
        "alerts": alerts
    })

@app.route('/api/health/history', methods=['GET'])
def get_health_history():
    conn = get_db_connection()
    # Pull all historical data, ordered chronologically
    result = conn.execute('SELECT * FROM health_logs ORDER BY id ASC')
    rows = result.fetchall()
    conn.close()

    history = []
    for row in rows:
        history.append({
            "timestamp": row['timestamp'],
            "systolic_bp": row['systolic_bp'],
            "diastolic_bp": row['diastolic_bp'],
            "effective_dose": row['effective_dose'],
            "t_score": row['t_score'],
            "sleep_hours": row['sleep_hours'],
            "ucla_total": row['ucla_1'] + row['ucla_2'] + row['ucla_3']
        })
    
    return jsonify(history)

#front end
@app.route('/')
def serve_frontend():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(port=8080,debug=True)
