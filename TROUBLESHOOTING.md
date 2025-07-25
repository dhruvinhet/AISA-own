# Troubleshooting Guide

## Common Issues and Solutions

### 1. API Connection Error: "Your default credentials were not found"

**Problem**: The system is trying to use Google Cloud Vertex AI instead of Google AI Studio.

**Solution**: 
- Make sure you have the correct API key from Google AI Studio (not Google Cloud)
- Get your API key from: https://aistudio.google.com/app/apikey
- Update your `.env` file with the correct key
- Run the test script: `python test_api.py`

### 2. Missing AI_STUDIO_API_KEY

**Problem**: Environment variable not set.

**Solution**:
1. Copy `.env.example` to `.env` in the backend directory
2. Edit `.env` and replace `your_ai_studio_api_key_here` with your actual API key
3. Restart the backend server

### 3. Module Import Errors

**Problem**: Python packages not installed correctly.

**Solution**:
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Frontend Connection Issues

**Problem**: Frontend can't connect to backend.

**Solution**:
1. Make sure backend is running on port 5000
2. Check that frontend `.env` has: `REACT_APP_API_BASE_URL=http://localhost:5000`
3. Verify CORS is enabled (it should be by default)

### 5. Port Already in Use

**Problem**: Port 5000 or 3000 is already in use.

**Solution**:
- For backend: Change port in `app.py` (line with `app.run`)
- For frontend: Use `npm start` and when prompted, choose a different port
- Update frontend `.env` if you change the backend port

### 6. JSON Parsing Errors

**Problem**: AI response is not valid JSON.

**Solution**: This is handled automatically - the system will display the raw response if JSON parsing fails.

## Testing Your Setup

### Test API Connection
```bash
cd backend
venv\Scripts\activate
python test_api.py
```

### Test Backend Endpoint
```bash
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a simple calculator app"}'
```

### Test Full System
1. Start backend: `cd backend && venv\Scripts\activate && python app.py`
2. Start frontend: `cd frontend && npm start`
3. Open http://localhost:3000
4. Enter a project description and click "Generate Plan"

## Getting Help

1. **Check Server Logs**: Look at the terminal where you're running the backend
2. **Check Browser Console**: Open Developer Tools in your browser
3. **Verify Environment**: Make sure all environment variables are set correctly
4. **Test API Key**: Use the `test_api.py` script to verify your API connection

## API Key Setup

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key (or use an existing one)
3. Copy the key to your `.env` file
4. Run `python test_api.py` to verify the connection

The API key should look like: `AIzaSyA...` (starts with AIzaSy)

## Rate Limits

Google AI Studio has usage limits:
- Free tier: 15 requests per minute
- If you hit rate limits, wait a minute and try again
- For production use, consider upgrading your plan
