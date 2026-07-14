from flask import Flask, render_template, request, jsonify
from utilities.exporter import make_img

app = Flask(__name__)

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