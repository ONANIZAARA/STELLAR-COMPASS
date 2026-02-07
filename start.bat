@echo off
echo.
echo ========================
echo  Stellar Compass Startup
echo ========================
echo.

REM Check if virtual environment exists
if not exist "backend\venv" (
    echo Creating virtual environment...
    cd backend
    python -m venv venv
    cd ..
)

REM Install dependencies
echo Installing dependencies...
cd backend
call venv\Scripts\activate
pip install -q -r requirements.txt

REM Start backend
echo Starting backend server...
start /B python app.py
cd ..

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
echo.
echo ========================================
echo  Stellar Compass is running!
echo ========================================
echo.
echo  Backend API: http://localhost:5000
echo  Frontend:    http://localhost:8080
echo.
echo  Press Ctrl+C to stop servers
echo ========================================
echo.

cd frontend
python -m http.server 8080
