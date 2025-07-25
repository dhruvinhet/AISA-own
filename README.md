# AI-Based Python Code Generator System

A sophisticated multi-agent system that uses CrewAI and Google AI Studio (Gemini 2.5 Flash) to automatically plan, generate, test, and package Python projects based on natural language descriptions.

## 🚀 Features

- **AI Planning Agent**: Analyzes user requirements and creates comprehensive project plans
- **Multi-Agent Architecture**: Uses CrewAI for managing specialized AI agents
- **LLM Integration**: Powered by Google AI Studio's Gemini 2.5 Flash model
- **React Frontend**: Clean, responsive web interface for user interaction
- **Python-Only Focus**: Specialized for generating Python projects
- **GUI Framework Selection**: Automatically chooses between Streamlit and Tkinter based on use case
- **Comprehensive Planning**: Generates detailed project structure, file breakdown, and implementation strategy

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React         │    │   Flask API     │    │   CrewAI        │
│   Frontend      │───▶│   Backend       │───▶│   Planning      │
│                 │    │                 │    │   Agent         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │   Google AI     │
                                              │   Studio        │
                                              │   (Gemini 2.5)  │
                                              └─────────────────┘
```

## 📋 Current Implementation: Planning Agent

The current implementation focuses on the **Planning Agent**, which:

1. **Requirement Analysis**: Takes natural language project descriptions
2. **Technical Planning**: Determines required libraries, Python version, and frameworks
3. **Structure Design**: Creates comprehensive folder and file structures
4. **Component Breakdown**: Details what each file should contain and its purpose
5. **Implementation Strategy**: Provides development phases and best practices

### Planning Agent Output Includes:

- **Project Overview**: Name, description, purpose, and target audience
- **Technical Requirements**: Python version, dependencies, GUI framework choice
- **Project Structure**: Complete folder hierarchy and organization
- **File Breakdown**: Detailed description of each file's purpose and contents
- **Implementation Strategy**: Development phases and critical components
- **Best Practices**: Code organization, error handling, and documentation guidelines

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- Google AI Studio API key

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your AI Studio API key
```

5. Run the backend:
```bash
python app.py
```

Backend will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
# Create .env file
echo "REACT_APP_API_BASE_URL=http://localhost:5000" > .env
```

4. Start the development server:
```bash
npm start
```

Frontend will be available at `http://localhost:3000`

## 🎯 Usage

1. **Start both backend and frontend servers**
2. **Open the web interface** at `http://localhost:3000`
3. **Enter your project description** in natural language
   - Example: "Create a web scraper that extracts product data from e-commerce websites and stores it in a database with a Streamlit dashboard for visualization"
4. **Click "Generate Plan"** to send the request to the Planning Agent
5. **Review the comprehensive plan** with expandable sections:
   - Project Overview
   - Technical Requirements
   - Project Structure
   - File Breakdown
   - Implementation Strategy
   - Best Practices

## 📁 Project Structure

```
AISA/
├── backend/
│   ├── app.py                    # Flask application entry point
│   ├── agents/
│   │   ├── __init__.py
│   │   └── planning_agent.py     # Planning Agent implementation
│   ├── requirements.txt          # Python dependencies
│   ├── .env.example             # Environment variables template
│   └── README.md                # Backend documentation
├── frontend/
│   ├── public/
│   │   └── index.html           # HTML template
│   ├── src/
│   │   ├── components/
│   │   │   └── PlanDisplay.js   # Plan visualization component
│   │   ├── App.js               # Main React application
│   │   ├── App.css              # Application styles
│   │   ├── index.js             # React entry point
│   │   └── index.css            # Global styles
│   ├── package.json             # Node.js dependencies
│   ├── tailwind.config.js       # Tailwind CSS configuration
│   └── README.md                # Frontend documentation
└── README.md                    # This file
```

## 🔧 Technologies Used

### Backend
- **Flask**: Web framework for API endpoints
- **CrewAI**: Multi-agent orchestration framework
- **Google AI Studio**: LLM API for Gemini 2.5 Flash
- **Python-dotenv**: Environment variable management

### Frontend
- **React 18**: User interface framework
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API calls
- **Lucide React**: Icon library

## 🌟 Future Enhancements

The system is designed to be extended with additional agents:

1. **Code Generation Agent**: Actually write the Python code based on the plan
2. **Testing Agent**: Generate comprehensive test suites
3. **Documentation Agent**: Create README files and code documentation
4. **Package Agent**: Handle project packaging and dependency management
5. **Quality Assurance Agent**: Code review and optimization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the README files in backend and frontend directories
2. Ensure all environment variables are properly configured
3. Verify that your AI Studio API key is valid and has sufficient quota
4. Check that both backend and frontend servers are running

## 🎉 Example Output

When you input: *"Create a weather dashboard that fetches data from an API and displays interactive charts"*

The Planning Agent will generate a comprehensive plan including:

- Project structure with separate modules for API handling, data processing, and visualization
- Technical requirements specifying Streamlit for the GUI (web-based dashboard)
- Required libraries like requests, pandas, plotly, and streamlit
- Detailed file breakdown explaining the purpose of each component
- Implementation strategy with prioritized development phases
- Best practices for API key management and error handling
