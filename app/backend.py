import sys
import os
import re
from flask import Flask, render_template, request, jsonify
from utilities.exporter import make_img

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
        if os.path.basename(base_path) == 'app':
            base_path = os.path.dirname(base_path)
    return os.path.join(base_path, relative_path)

app = Flask(__name__,
            template_folder=resource_path('templates'),
            static_folder=resource_path('static'))

# ---------- Storage directory (HARDCODE YOUR DESIRED PATH) ----------
STORAGE_DIR = r"D:/projects/diagramappfornotes/noteimg"   # <-- CHANGE IF NEEDED
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_canvas():
    try:
        payload = request.get_json()
        if not payload:
            return jsonify({"error": "No data received"}), 400

        saved_path = make_img(payload, output_dir=STORAGE_DIR)   # pass storage dir
        return jsonify({"status": "success", "path": saved_path}), 200

    except Exception as e:
        print(f"[ERROR] Failed to process payload: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# -DISCLAIMER--------- DO NOT run with debug=True here ----------