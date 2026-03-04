@echo off
echo Starting GS API Test Platform (using global Python)...
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
    echo Creating backend\.env from example...
    copy "backend\.env.example" "backend\.env"
    echo.
    echo IMPORTANT: Edit backend\.env and add your Azure OpenAI credentials!
    echo.
    notepad backend\.env
    echo.
    echo Press any key after saving your credentials...
    pause >nul
)

REM Start backend in new window
echo Starting Backend Server (http://localhost:8000)...
start "GS API Backend" cmd /c "cd backend && python main.py"

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in new window
echo Starting Frontend Server (http://localhost:5173)...
start "GS API Frontend" cmd /c "cd frontend && npm run dev"

echo.
echo ========================================
echo Both servers are running!
echo ========================================
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo ========================================
echo.
echo Close the server windows to stop the application.
echo Press any key to exit this launcher...
pause >nul
