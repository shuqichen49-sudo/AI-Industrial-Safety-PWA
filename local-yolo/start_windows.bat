@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo [1/3] Creating Python virtual environment...
  py -3.11 -m venv .venv
  if errorlevel 1 (
    echo Python 3.11 was not found. Install Python 3.11 x64 and try again.
    pause
    exit /b 1
  )
)

echo [2/3] Installing or checking dependencies...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
  echo Dependency installation failed.
  pause
  exit /b 1
)

if not exist "models" mkdir models
if not exist "models\best.pt" (
  echo.
  echo NOTE: No custom PPE model found.
  echo The app will use yolov8n.pt as a general person-detection demo only.
  echo Put your validated PPE model at: local-yolo\models\best.pt
)

echo [3/3] Starting local webcam detection app...
start "" http://127.0.0.1:8000
".venv\Scripts\python.exe" -m uvicorn app:app --host 127.0.0.1 --port 8000
pause
