# AI-based Python Code Generator System - Backend

This is the backend service for the multi-agent AI-based Python code generator system.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env file and add your AI Studio API key
```

4. Run the application:
```bash
python app.py
```

The backend will be available at `http://localhost:5000`

## API Endpoints

### POST /api/plan
Create a project plan based on user prompt.

**Request:**
```json
{
  "prompt": "Create a web scraper that extracts data from e-commerce websites"
}
```

**Response:**
```json
{
  "success": true,
  "plan": {
    "project_overview": {...},
    "technical_requirements": {...},
    "project_structure": {...},
    "file_breakdown": {...},
    "implementation_strategy": {...},
    "best_practices": {...}
  }
}
```

### GET /api/health
Health check endpoint.

## Project Structure

```
backend/
├── app.py                 # Main Flask application
├── agents/
│   └── planning_agent.py  # Planning Agent implementation
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```
