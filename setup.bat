@echo off
echo ========================================
echo GS API Test Platform - Setup Script
echo ========================================
echo.

echo [1/4] Setting up Backend...
cd backend

REM Remove old venv if exists
if exist "venv" (
    echo Removing old virtual environment...
    rmdir /s /q venv
)

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install backend dependencies
    pause
    exit /b 1
)

echo Backend setup complete!
echo.

cd ..

echo [2/4] Setting up Frontend...
cd frontend

echo Installing Node dependencies...
call npm install

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install frontend dependencies
    pause
    exit /b 1
)

echo Frontend setup complete!
echo.

cd ..

echo [3/4] Creating .env file...
if not exist "backend\.env" (
    copy "backend\.env.example" "backend\.env"
    echo Created backend\.env - Please update with your Azure OpenAI credentials
) else (
    echo backend\.env already exists
)

echo.
echo [4/4] Setup Summary
echo ========================================
echo Backend: Ready (Virtual environment created with all dependencies)
echo Frontend: Ready (Node modules installed)
echo.
echo IMPORTANT: Edit backend\.env and add your Azure OpenAI credentials:
echo   - AZURE_OPENAI_ENDPOINT
echo   - AZURE_OPENAI_API_KEY
echo   - AZURE_OPENAI_DEPLOYMENT_NAME
echo.
echo To start the application, run: start.bat
echo ========================================
echo.
pause
