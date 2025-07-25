# AI Python Code Generator - Frontend

This is the React frontend for the multi-agent AI-based Python code generator system.

## Features

- Clean and intuitive user interface
- Real-time project plan generation
- Expandable sections for detailed plan viewing
- Responsive design with Tailwind CSS
- Error handling and loading states

## Setup

1. Install Node.js (v16 or higher)

2. Install dependencies:
```bash
npm install
```

3. Create environment variables:
```bash
# Create .env file in the frontend directory
REACT_APP_API_BASE_URL=http://localhost:5000
```

4. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Usage

1. Enter a natural language description of your Python project
2. Click "Generate Plan" to send the request to the AI Planning Agent
3. View the comprehensive project plan with expandable sections:
   - Project Overview
   - Technical Requirements
   - Project Structure
   - File Breakdown
   - Implementation Strategy
   - Best Practices

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   └── PlanDisplay.js    # Component for displaying generated plans
│   ├── App.js                # Main application component
│   ├── App.css              # Application styles
│   ├── index.js             # React entry point
│   └── index.css            # Global styles with Tailwind
├── package.json             # Dependencies and scripts
├── tailwind.config.js       # Tailwind CSS configuration
└── postcss.config.js        # PostCSS configuration
```

## Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App (not recommended)

## Technologies Used

- React 18
- Tailwind CSS
- Axios for API calls
- Lucide React for icons
