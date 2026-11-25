@echo off
python -m pip install -r requirements.txt
python -m pip install pyinstaller
pyinstaller --noconfirm --clean --onefile --windowed --name VidMotive main.py
echo.
echo EXE created at dist\VidMotive.exe
pause
