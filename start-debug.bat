@echo off
echo ========================================
echo GS API Test Platform - Debug Mode
echo ========================================
echo.

REM Check prerequisites
if not exist "frontend\node_modules" (
    echo ERROR: Frontend dependencies not installed
    echo Run: cd frontend && npm install
    pause
    exit /b 1
)

if not exist "backend\.env" (
    echo Creating .env file...
    copy "backend\.env.example" "backend\.env"
    echo.
    echo Please edit backend\.env with your Azure OpenAI credentials
    notepad backend\.env
)

echo.
echo Starting Backend Server...
echo Check the backend window for any errors
echo.
start "Backend - DO NOT CLOSE" cmd /k "cd backend && echo Starting FastAPI server... && python main.py || (echo. && echo ERROR: Backend failed to start! && echo Check the error above && pause)"

timeout /t 5 /nobreak >nul

echo.
echo Starting Frontend Server...
echo.
start "Frontend - DO NOT CLOSE" cmd /k "cd frontend && echo Starting Vite dev server... && npm run dev || (echo. && echo ERROR: Frontend failed to start! && pause)"

echo.
echo ========================================
echo Servers starting in separate windows
echo ========================================
echo.
echo If you see errors in the server windows:
echo - Backend errors: Check Python dependencies and .env file
echo - Frontend errors: Check node_modules installation
echo.
echo Access the application at:
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo.
echo ========================================
pause
