import sys
import os
import re
from flask import Flask, render_template, request, jsonify
from utilities.exporter import make_img
from werkzeug.utils import secure_filename

#making executable application file

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

'''attention here: storage directory'''
STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)),'storage') #CHNAGE THIS LINE TO CHANGE STORAGE LOCATION

if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)





    #main functionality

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_canvas():
    try:
        payload = request.get_json()
        if not payload:
            return jsonify({"error": "No data received"}), 400 

        saved_path = make_img(payload)

        return jsonify({"status": "success", "path": saved_path}), 200

    except Exception as e:
        print(f"[ERROR] Failed to process payload: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)