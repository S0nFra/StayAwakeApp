pyinstaller --noconsole --onefile ^
    --add-data "icon\*.png;." ^
    .\app.py

if not exist "%cd%\dist\icon" (
    echo:
    echo # Manual copy
    mkdir "%cd%\dist\icon"
    copy "%cd%\icon\*" "%cd%\dist\icon"
)