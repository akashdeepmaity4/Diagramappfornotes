import sys
import os
import re
from flask import Flask, render_template, request, jsonify

import os
import time
from PIL import Image, ImageDraw

def make_img(payload, output_dir="noteimg"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    width = payload.get("width", 800)
    height = payload.get("height", 600)

    image = Image.new("RGBA", (width, height), "white")
    draw = ImageDraw.Draw(image)

    lines = payload.get("lines", [])
    for line in lines:
        color = line.get("color", "#000000")
        points = line.get("points", [])

        coord_tuples = [(pt["x"], pt["y"]) for pt in points]

        if len(coord_tuples) >= 2:
            draw.line(coord_tuples, fill=color, width=3, joint="round")
        elif len(coord_tuples) == 1:
            x, y = coord_tuples[0]
            draw.ellipse([x-2, y-2, x+2, y+2], fill=color)
        else: 
            pass
    timestamp = int(time.time())
    filename = f"note_{timestamp}.png"
    filepath = os.path.join(output_dir, filename)

    image.save(filepath, "PNG")
    print(f"[SUCCESS] Exported vector plot to disk: {filepath}")
    return filepath

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
#will be adding way to set this dynamically in future updates
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

        saved_path = make_img(payload, output_dir=STORAGE_DIR) 
        return jsonify({"status": "success", "path": saved_path}), 200

    except Exception as e:
        print(f"[ERROR] Failed to process payload: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
        

# -DISCLAIMER--------- DO NOT run with debug=True here ----------