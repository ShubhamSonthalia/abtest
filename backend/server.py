from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import csv
import os

# The static_folder argument tells Flask where to find the frontend files.
# The path is relative to the 'backend' directory.
app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

DATA_FILE = "events.csv"

# Initialize CSV if it doesn't exist in the 'backend' directory
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["visitor_id", "variant", "event_type", "timestamp"])

@app.route("/")
def index():
    # Serve index.html from the static_folder ('../frontend')
    return app.send_static_file('index.html')

@app.route("/log", methods=["POST"])
def log_event():
    data = request.get_json()
    required = ["visitor_id", "variant", "event_type", "timestamp"]
    if not all(k in data for k in required):
        return jsonify({"status": "error", "message": "Missing fields"}), 400
    
    # Write to events.csv in the 'backend' directory
    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            data["visitor_id"],
            data["variant"],
            data["event_type"],
            data["timestamp"]
        ])
    return jsonify({"status": "success"}), 200

# This part is needed to run the app locally for testing
if __name__ == "__main__":
    app.run(debug=True)