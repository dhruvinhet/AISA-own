@echo off
echo ========================================
echo Starting AI Python Code Generator
echo ========================================
echo.

echo Starting Backend Server...
start "Backend Server" cmd /k "cd backend && venv\Scripts\activate && python app.py"

echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && npm start"

echo.
echo Both servers are starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo The application will open automatically in your browser.
echo.
pause
