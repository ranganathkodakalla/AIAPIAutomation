@echo off
echo ========================================
echo GS API Test Platform
echo ========================================
echo.

echo Killing existing processes...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
timeout /t 2 /nobreak >nul

REM Check if node_modules exists
if not exist "frontend\node_modules" (
    echo ERROR: Node modules not found
    echo Run: cd frontend ^&^& npm install
    pause
    exit /b 1
)

REM Check if .env exists
if not exist "backend\.env" (
    echo Creating .env file...
    copy "backend\.env.example" "backend\.env"
    echo.
    echo IMPORTANT: Edit backend\.env with your Azure OpenAI credentials
    echo.
)

echo Starting Backend Server on port 8000...
start "GS API Backend - DO NOT CLOSE" powershell -NoExit -Command "cd backend; python main.py"

timeout /t 4 /nobreak >nul

echo Starting Frontend Server on port 5000...
start "GS API Frontend - DO NOT CLOSE" powershell -NoExit -Command "cd frontend; $env:PORT=5000; npm run dev -- --port 5000"

echo.
echo ========================================
echo Servers Started!
echo ========================================
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5000
echo API Docs: http://localhost:8000/docs
echo ========================================
echo.
echo Close the server windows to stop the application.
pause
