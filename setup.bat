@echo off
echo ========================================
echo AI Python Code Generator Setup
echo ========================================
echo.

echo Setting up Backend...
cd backend
echo Creating virtual environment...
python -m venv venv
echo Activating virtual environment...
call venv\Scripts\activate
echo Installing Python dependencies...
pip install -r requirements.txt
echo.

echo Backend setup complete!
echo.
echo IMPORTANT: Configure your API key now!
echo.
echo 1. Copy .env.example to .env:
copy .env.example .env
echo.
echo 2. Edit the .env file and replace 'your_ai_studio_api_key_here' with your actual API key
echo    Get your API key from: https://aistudio.google.com/app/apikey
echo.
echo 3. Test your API connection:
echo    python test_api.py
echo.

cd ..
echo Setting up Frontend...
cd frontend
echo Installing Node.js dependencies...
call npm install
echo.

echo Frontend setup complete!
echo.
echo Creating frontend .env file...
echo REACT_APP_API_BASE_URL=http://localhost:5000 > .env
echo.

cd ..
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo NEXT STEPS:
echo 1. Configure your Google AI Studio API key in backend/.env
echo 2. Test the API connection: cd backend && python test_api.py
echo 3. Start the system: start.bat
echo.
echo The application will be available at http://localhost:3000
echo.
pause
