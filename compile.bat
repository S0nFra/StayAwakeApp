pyinstaller --noconsole --onefile .\app.py

if not exist "%cd%\dist\icon" (
    echo:
    echo # Manual copy
    mkdir "%cd%\dist\icon"
    copy "%cd%\icon\*" "%cd%\dist\icon"
)