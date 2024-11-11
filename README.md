# StayAwakeApp

A system tray application to keep your Windows PC awake.

## ⚡ Key Features

- Prevents PC from entering sleep mode
- Starts automatically with Windows
- Minimal interface with system tray icon
- Light on system resources

## ⚠️ Important Notes

- Currently only available for Windows 10/11
- The application modifies power settings only while running
- Closing the application restores default system settings
- The application doesn't interfere with manual PC shutdown

## 🚀 Quick Installation

1. Download the executable from the [latest release](https://github.com/S0nFra/StayAwakeApp/releases/latest)
2. Open Windows startup folder:
   - Press `Win + R`
   - Type `shell:startup`
   - Press `Enter`
3. Copy `StayAwakeApp.exe` into the opened folder
4. Double-click `StayAwakeApp.exe` to start the application immediately

> **Info**: The startup folder contains programs that Windows runs automatically at system startup. By placing the application here, it will automatically start every time you turn on your PC.

## 🛠️ Building from source

You can generate the executable by building the project from scratch using Windows:

```bash
./compile.bat
```

## 💡 How it works

The application runs in the background and appears as an icon in the system tray. Once installed in the startup folder, it will automatically run every time Windows starts.

## 📝 License

MIT License - see the [LICENSE](LICENSE) file for details

---
💻 Made with ❤️ to keep your PC always awake
