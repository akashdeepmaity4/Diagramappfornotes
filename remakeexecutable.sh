cd D:\projects\diagramappfornotes
rmdir /s build
rmdir /s dist
del *.spec
pyinstaller --onefile --windowed --add-data "templates;templates" --add-data "static;static" --add-data "app;backend" --add-data "noteimg;noteimg" --hidden-import flask --hidden-import jinja2 --hidden-import app --hidden-import app.backend --pathsx . launcher.py