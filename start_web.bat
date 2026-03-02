@echo off
echo ================================
echo JanSahayak - Starting Web Server
echo ================================
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo Virtual environment not found!
    echo Please run setup first.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Start Flask app
echo Starting Flask application...
echo.
python app.py

pause
