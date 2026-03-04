@echo off
echo ========================================
echo GS API Test Platform - Simple Setup
echo ========================================
echo.

echo [1/3] Setting up Backend Virtual Environment...
cd backend

REM Remove old venv if exists
if exist "venv" (
    echo Removing old virtual environment...
    rmdir /s /q venv
)

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment and installing packages...
call venv\Scripts\activate.bat && pip install fastapi uvicorn sqlalchemy pandas openpyxl openai python-multipart

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to install backend dependencies
    echo Try running PowerShell or Command Prompt as Administrator
    pause
    exit /b 1
)

echo Backend setup complete!
cd ..

echo.
echo [2/3] Setting up Frontend...
cd frontend

if not exist "node_modules" (
    echo Installing Node dependencies...
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to install frontend dependencies
        pause
        exit /b 1
    )
) else (
    echo Node modules already installed
)

echo Frontend setup complete!
cd ..

echo.
echo [3/3] Creating .env file...
if not exist "backend\.env" (
    copy "backend\.env.example" "backend\.env"
    echo Created backend\.env
) else (
    echo backend\.env already exists
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo NEXT STEPS:
echo 1. Edit backend\.env and add your Azure OpenAI credentials
echo 2. Run: start.bat
echo ========================================
echo.
pause
