pyinstaller --noconsole --onefile ^
    --add-data ".\icon\*.png;img" ^
    .\app.py