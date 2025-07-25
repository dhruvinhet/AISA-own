import React from 'react';
import PlanDisplay from './components/PlanDisplay';

// Test data that matches the structure returned by Gemini
const testPlan = {
  "best_practices": {
    "code_organization": "Follow PEP 8 guidelines for code style. Use meaningful variable names and comments to improve readability.",
    "configuration_management": "For this simple project, configuration management is not necessary. However, for more complex projects, consider using environment variables or configuration files.",
    "documentation_requirements": "For this simple project, a basic README file explaining how to run the application is sufficient. For more complex projects, include detailed documentation for each module and function.",
    "error_handling": "Implement `try-except` blocks to handle potential errors, such as division by zero or invalid input."
  },
  "file_breakdown": {
    "calculator.py": {
      "dependencies": ["tkinter"],
      "interactions": "This is the main entry point of the application. It imports functions from other modules if any.",
      "purpose": "Main application logic and GUI implementation using Tkinter."
    },
    "test_calculator.py": {
      "dependencies": ["unittest", "src/calculator.py (import functions)"],
      "interactions": "Tests the functions defined in calculator.py",
      "purpose": "Unit tests for the calculator functions."
    }
  },
  "implementation_strategy": {
    "critical_components": ["Tkinter GUI setup", "Calculation logic"],
    "deployment_considerations": "Since it's a Tkinter application, it can be run directly on any system with Python and Tkinter installed.",
    "development_phases": ["1. Set up project structure and Tkinter window.", "2. Implement number and operator buttons.", "3. Add calculation logic.", "4. Implement error handling.", "5. Add unit tests.", "6. Final testing and documentation."],
    "test_file_requirements": "The `test_calculator.py` file should contain test functions for each operation (addition, subtraction, multiplication, division) and edge cases (division by zero, invalid input).",
    "testing_strategy": "Use the `unittest` module to create unit tests for each arithmetic operation. Test for normal cases and edge cases like division by zero."
  },
  "project_description": "A basic calculator application that performs standard arithmetic operations. It provides a user-friendly graphical interface built with Tkinter.",
  "project_name": "Simple Calculator App",
  "project_structure": {
    "directories": [
      {"name": "src", "purpose": "Contains the main source code of the calculator application."},
      {"name": "tests", "purpose": "Contains unit tests for the application."}
    ],
    "files": [
      {"entry_point": true, "path": "calculator_app/src/calculator.py", "purpose": "Main application logic and GUI."},
      {"path": "calculator_app/tests/test_calculator.py", "purpose": "Unit tests for calculator functions."},
      {"path": "calculator_app/README.md", "purpose": "Project documentation and usage instructions."}
    ],
    "root_directory": "calculator_app"
  },
  "target_audience": "Individuals needing a quick and easy tool for performing basic calculations, students learning programming concepts.",
  "technical_requirements": {
    "database_requirements": "None",
    "dependencies": [],
    "external_apis": "None",
    "gui_framework": "Tkinter",
    "gui_framework_justification": "Tkinter is chosen for its simplicity and suitability for creating basic desktop applications. It's lightweight and comes pre-installed with Python.",
    "python_version": "3.9+"
  }
};

function TestPlanDisplay() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8">Test Plan Display</h1>
        <PlanDisplay plan={testPlan} />
      </div>
    </div>
  );
}

export default TestPlanDisplay;
