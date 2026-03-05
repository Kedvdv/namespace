@echo off
setlocal

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

pyinstaller --noconfirm --onefile --windowed --name namespace main.py

echo.
echo Build complete. EXE is in dist\namespace.exe
endlocal
