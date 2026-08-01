import sys
import os
import threading
import time
import webview

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)

from app.backend import app

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    time.sleep(1)

    webview.create_window(
        'Diagram App for Notes',
        'http://127.0.0.1:5000',
        width=1024,
        height=768,
        resizable=True
    )
    webview.start()