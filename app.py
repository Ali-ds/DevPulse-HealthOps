from flask import Flask, jsonify
import random, time, math

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "running", "message": "DS Monitor App"})

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

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)