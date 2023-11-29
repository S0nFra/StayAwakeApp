#!/bin/bash

# Run PyInstaller to create the executable
pyinstaller --noconsole --onefile \
    --add-data "icon/*.png:img" \
    ./app.py
