@echo off
echo ========================================
echo Restarting AI Python Code Generator
echo ========================================
echo.

echo Stopping any existing processes...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im node.exe >nul 2>&1

echo.
echo Starting Backend Server...
start "Backend Server" cmd /k "cd f:\AISA\backend && venv\Scripts\activate && python app.py"

echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo Testing backend...
cd f:\AISA\backend
python test_backend.py

echo.
echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd f:\AISA\frontend && npm start"

echo.
echo ========================================
echo System Restarted!
echo ========================================
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo The application should now be working properly.
echo Check the backend terminal for debugging output.
echo.
pause
