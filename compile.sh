pyinstaller --noconsole --onefile .\app.py

# Get the full path of the script
ws=$(readlink -f "$0")

# Check if the destination folder exists
if [ ! -d "$ws/dist/icon" ]; then
    echo
    echo "Manual copy"

    # Create the destination folder
    mkdir -p "$ws/dist/icon"

    # Copy files from the source folder to the destination folder
    cp -r "$ws/icon"/* "$ws/dist/icon"
fi