set -e

PROJECT_DIR="D:/projects/diagramappfornotes"
cd "$PROJECT_DIR" || { echo "Directory not found"; exit 1; }

echo "cleaning"
rm -rf build dist
rm -f *.spec

echo "Building exe"
pyinstaller \
    --onefile \
    --windowed \
    --add-data "templates;templates" \
    --add-data "static;static" \
    --add-data "app;app" \
    --add-data "utilities;utilities" \
    --hidden-import flask \
    --hidden-import jinja2 \
    --hidden-import werkzeug \
    --hidden-import webview \
    --hidden-import app.backend \
    --hidden-import utilities.exporter \
    --hidden-import PIL \
    --hidden-import PIL.Image \
    --hidden-import PIL.ImageDraw \
    launcher.py

echo "✅ Build complete! Check dist/DiagramApp.exe"