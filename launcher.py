import sys
import os
import socket
import threading
import time
import webview

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)

from app.backend import app
from werkzeug.serving import make_server

HOST = '127.0.0.1'
PORT = 5000

# Holds the werkzeug server handle so we can shut it down cleanly when the
# webview window closes (avoids leaving a stale Flask process on the port).
_server = None


def is_port_in_use(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0


def wait_for_server(host, port, timeout=15):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if is_port_in_use(host, port):
            return True
        time.sleep(0.2)
    return False


def start_flask(host=HOST, port=PORT):
    """Start Flask via werkzeug.make_server so we get a shutdownable handle."""
    global _server
    _server = make_server(host, port, app, threaded=True)
    _server.serve_forever()


def on_window_closed():
    """Called by pywebview when the window is closed -> stop Flask too."""
    if _server is not None:
        try:
            _server.shutdown()       # stop serve_forever() loop
        except Exception:
            pass
        try:
            _server.server_close()   # release the listening socket
        except Exception:
            pass
    # Give the daemon thread a moment to unwind, then exit hard so no stale
    # python process is left holding the port.
    threading.Timer(0.5, os._exit, args=(0,)).start()


if __name__ == '__main__':
    port_busy = is_port_in_use(HOST, PORT)

    if port_busy:
        # Something is already listening on the port (e.g. a standalone
        # `python -m app.backend` you started to test, or a previous run).
        # Reuse it instead of aborting, so the webview still opens.
        print(f"[INFO] Port {PORT} already in use - reusing existing server.")
    else:
        flask_thread = threading.Thread(target=start_flask, daemon=True)
        flask_thread.start()

        # Wait until Flask is actually accepting connections instead of a fixed
        # sleep, so the webview never loads a dead/connection-refused page.
        if not wait_for_server(HOST, PORT, timeout=15):
            print("[ERROR] Flask server failed to start within 15s.")
            sys.exit(1)

    window = webview.create_window(
        'Diagram App for Notes',
        f'http://{HOST}:{PORT}',
        width=1024,
        height=768,
        resizable=True
    )
    window.events.closing += on_window_closed
    webview.start()