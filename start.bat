@echo off
echo Starting Backend Authentication API...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install requirements
echo Installing/updating requirements...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and configure your settings.
    echo.
    pause
    exit /b 1
)

REM Start the application
echo.
echo Starting the API server...
echo API will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
python main.py
