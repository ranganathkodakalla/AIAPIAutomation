@echo off
echo Starting GS API Test Platform (without virtual environment)...
echo.

REM Check if node_modules exists
if not exist "frontend\node_modules" (
    echo ERROR: Node modules not found in frontend\node_modules
    echo Please install them first: cd frontend && npm install
    pause
    exit /b 1
)

REM Check if .env exists
if not exist "backend\.env" (
    echo WARNING: backend\.env not found, creating from example...
    copy "backend\.env.example" "backend\.env"
    echo.
    echo IMPORTANT: Edit backend\.env and add your Azure OpenAI credentials before continuing!
    echo Press any key to continue anyway...
    pause >nul
)

REM Start backend in new window (without venv)
echo Starting Backend Server...
start "GS API Backend" cmd /k "cd backend && if defined VIRTUAL_ENV (deactivate) && python main.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in new window
echo Starting Frontend Server...
start "GS API Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Both servers are starting in separate windows:
echo - Backend: http://localhost:8000
echo - Frontend: http://localhost:5173
echo.
echo Press any key to exit this window (servers will continue running)...
pause >nul
