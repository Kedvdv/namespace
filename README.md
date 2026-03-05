# namespace chat app

A modern desktop chat application called **namespace** built with Python/Tkinter, including a Windows `.exe` build workflow.

## Features

- Clean dark UI with sidebar channels and message bubbles
- Real-time send flow with Enter key shortcut
- Auto echo-bot responses to simulate conversation
- Channel switching with contextual system message
- Ready-to-package build script for Windows executable output

## Run locally

```bash
python main.py
```

## Build Windows EXE

From a Windows terminal:

```bat
build_exe.bat
```

Output executable:

```text
dist\namespace.exe
```

## Manual build command

```bash
python -m pip install pyinstaller
pyinstaller --onefile --windowed --name namespace main.py
```
