import os
import sys
import webview

#incomplete

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.backend import backend
    print("Successfully imported app from app.app")
except ImportError as e:
    print(f"Import error: {e}")
    print("Files in current directory:", os.listdir('.'))
    sys.exit(1)
else:
    print("ERROR: check launcher.py")

if __name__ == '__main__':
    webview.create_window('Diagram App for Notes', app)
    webview.start()
