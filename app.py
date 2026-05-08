from flask import Flask, jsonify, request
from flask import render_template
from datetime import datetime
import random, time, math
from applicationinsights import TelemetryClient

tc = TelemetryClient('5949bebf-7d9a-4cd7-bc99-771dfc747efd')



app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('ehr_dashboard.html')

app.route('/patients')
def patients():
    return render_template('patients.html')
 
@app.route('/emergency')
def emergency():
    return render_template('emergency.html')
 
@app.route('/appointments')
def appointments_page():
    return render_template('appointments.html')
 
@app.route('/lab')
def lab_page():
    return render_template('lab.html')


@app.route('/load')
def generate_load():
    # Burns CPU — triggers your alerts
    result = sum(math.sqrt(i) for i in range(500000))
    return jsonify({"result": result})

@app.route('/error')
def generate_error():
    # Triggers exception alerts
    raise ValueError("Simulated error for monitoring demo")

@app.route('/slow')
def slow_response():
    # Triggers response time alerts
    time.sleep(random.uniform(2, 5))
    return jsonify({"message": "slow response simulated"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/patient/records')
def patient_records():
    # Simulate EHR database latency
    latency = random.uniform(0.05, 0.3)
    time.sleep(latency)
    return jsonify({"status": "ok", "records": 142, "latency_ms": latency*1000})


@app.route('/api/patient/emergency')
def emergency_traffic():
    # Simulate emergency spike — high load
    time.sleep(random.uniform(1.5, 3.0))
    return jsonify({"status": "ok", "type": "emergency", "queue": random.randint(20,50)})

@app.route('/api/ehr/status')
def ehr_status():
    # Simulate EHR system health check
    uptime = random.choice([True, True, True, False])  # 75% uptime for demo
    if not uptime:
        return jsonify({"status": "degraded"}), 503
    return jsonify({"status": "healthy", "uptime_pct": 99.7})

@app.route('/api/deployment/webhook', methods=['POST'])
def deployment_webhook():
    data     = request.json or {}
    status   = data.get('status',      'unknown')
    version  = data.get('version',     'unknown')
    stage    = data.get('stage',       'unknown')
    triggered= data.get('triggered_by','system')
 
    print(
        f"DEVPULSE_DEPLOYMENT | "
        f"status={status} | "
        f"version={version[:8]} | "
        f"stage={stage} | "
        f"triggered_by={triggered} | "
        f"timestamp={datetime.utcnow().isoformat()}",
        flush=True
    )
 
    if status == 'failed':
        print(
            f"DEVPULSE_ALERT | severity=critical | "
            f"message=Deployment failed for version {version[:8]}",
            flush=True
        )
 
    return jsonify({
        "received":  True,
        "status":    status,
        "version":   version[:8],
        "timestamp": datetime.utcnow().isoformat()
    })
# Database latency simulation (mentioned in problem statement)
@app.route('/api/db/query')
def db_query():
    latency = random.uniform(0.1, 0.8)
    time.sleep(latency)
    return jsonify({"status": "ok", "query_time_ms": round(latency*1000, 2),
                    "rows_returned": random.randint(10, 500)})

# EHR system uptime check
@app.route('/api/ehr/uptime')
def ehr_uptime():
    healthy = random.choices([True, False], weights=[90, 10])[0]
    if not healthy:
        return jsonify({"status": "down", "uptime_pct": 94.2}), 503
    return jsonify({"status": "healthy", "uptime_pct": 99.7})

# Appointment scheduling system
@app.route('/api/appointments')
def appointments():
    time.sleep(random.uniform(0.05, 0.2))
    return jsonify({"status": "ok", "scheduled": random.randint(80, 200),
                    "pending": random.randint(0, 15)})

# IT team notification endpoint
@app.route('/api/notify', methods=['POST'])
def notify():
    data = request.json
    app.logger.warning(f"IT_ALERT: severity={data.get('severity')} "
                       f"message={data.get('message')}")
    return jsonify({"notified": True, "timestamp": datetime.utcnow().isoformat()})

# System health summary — used by dashboard KPI cards
@app.route('/api/health/summary')
def health_summary():
    return jsonify({
        "ehr_status":       "healthy",
        "api_latency_ms":   random.uniform(80, 300),
        "db_latency_ms":    random.uniform(10, 150),
        "active_alerts":    random.randint(0, 3),
        "uptime_pct":       99.7
    })

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)