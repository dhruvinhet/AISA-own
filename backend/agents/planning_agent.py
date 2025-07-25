import google.generativeai as genai
import os
from typing import Dict, List, Any
import json

class PlanningAgent:
    def __init__(self):
        """
        Initialize the Planning Agent with Google AI Studio
        """
        # Configure Google AI Studio API
        api_key = os.getenv('AI_STUDIO_API_KEY')
        if not api_key:
            raise ValueError("AI_STUDIO_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        
        # Initialize the Gemini model
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Configure generation settings
        self.generation_config = {
            "temperature": 0.3,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
    
    def create_project_plan(self, user_prompt: str) -> Dict[str, Any]:
        """
        Create a comprehensive project plan based on user prompt
        
        Args:
            user_prompt (str): Natural language description of the desired project
            
        Returns:
            Dict[str, Any]: Comprehensive project plan
        """
        
        try:
            # Create the system prompt for the planning task
            system_prompt = """You are a Senior Python Project Planner, an expert Python developer and project architect with years of experience 
            in designing and structuring Python projects. You excel at breaking down complex requirements 
            into well-organized, modular project structures. You understand best practices for Python 
            project organization, dependency management, and code architecture.

            Your task is to analyze user requirements and create detailed project plans that include comprehensive 
            technical specifications, project structure, and implementation strategies."""

            # Create the detailed planning prompt
            planning_prompt = f"""
            Based on the following user requirement, create a comprehensive Python project plan:
            
            USER REQUIREMENT: {user_prompt}
            
            Your task is to analyze this requirement and create a detailed project plan that includes:
            
            1. PROJECT OVERVIEW:
               - Project name and description
               - Main functionality and purpose
               - Target audience or use case
            
            2. TECHNICAL REQUIREMENTS:
               - Required Python libraries and dependencies
               - Recommended Python version
               - GUI framework choice: Analyze if the project needs a GUI. If yes, choose Streamlit (for web-based, data-driven apps) or Tkinter (for desktop applications). If no GUI needed, specify 'None'.
               - Database requirements (if any)
               - External APIs or services needed
            
            3. PROJECT STRUCTURE:
               - Complete folder and file structure
               - Purpose and responsibility of each directory
               - Main entry points and configuration files
            
            4. FILE BREAKDOWN:
               - For each Python file that needs to be created:
                 * File path and name
                 * Primary purpose and functionality
                 * Key classes, functions, or components it should contain
                 * Dependencies and imports needed
                 * How it interacts with other files
            
            5. IMPLEMENTATION STRATEGY:
               - Development phases and order of implementation
               - Critical components that should be built first
               - Testing strategy and test file requirements
               - Deployment considerations
            
            6. BEST PRACTICES:
               - Code organization principles to follow
               - Error handling strategies
               - Configuration management approach
               - Documentation requirements
            
            IMPORTANT CONSTRAINTS:
            - Only generate plans for Python projects
            - For GUI applications, choose between Streamlit (for web-based, data-driven apps) or Tkinter (for desktop applications)
            - Follow Python best practices and PEP standards
            - Ensure the project structure is modular and maintainable
            - Include appropriate testing structure
            
            CRITICAL: You MUST respond with ONLY a valid JSON object matching this EXACT schema. Do not include any markdown formatting, code blocks, or explanatory text. All values must be strings (no nested objects or arrays except where explicitly specified):

            {{
                "project_overview": {{
                    "name": "string - project name",
                    "description": "string - detailed project description",
                    "purpose": "string - main functionality and purpose",
                    "audience": "string - target audience or use case"
                }},
                "technical_requirements": {{
                    "python_version": "string - recommended Python version (e.g., '3.9', '3.10', '3.11')",
                    "dependencies": "string - comma-separated list of required libraries",
                    "gui_framework": "string - REQUIRED: Choose 'Streamlit' for web apps, 'Tkinter' for desktop apps, or 'None' if no GUI needed",
                    "gui_framework_justification": "string - REQUIRED: Explain why this GUI choice was made or why no GUI is needed",
                    "database_requirements": "string - database needs description or 'None'",
                    "external_apis": "string - external APIs needed or 'None'",
                    "system_requirements": "string - any special system requirements or 'Standard Python environment'"
                }},
                "project_structure": {{
                    "root_directory": "string - name of the main project directory",
                    "description": "string - overall structure description",
                    "folders": "string - detailed folder structure as text"
                }},
                "file_breakdown": "string - MANDATORY: Detailed breakdown of ALL files to be created with their exact paths, primary purposes, key functions/classes, dependencies, and file interactions. Format as structured text with clear file sections.",
                "implementation_strategy": {{
                    "development_phases": "string - ordered list of development phases",
                    "test_file_requirements": "string - testing strategy and test files needed"
                }}
            }}

            IMPORTANT: The file_breakdown field is MANDATORY and must contain detailed information about every file in the project. Do not omit this field.

            Return ONLY the JSON object with no additional text, markdown formatting, or code blocks.
            """

            print("🚀 Sending request to Gemini API...")
            
            # Generate the response using Gemini
            full_prompt = f"{system_prompt}\n\n{planning_prompt}"
            response = self.model.generate_content(
                full_prompt,
                generation_config=self.generation_config
            )
            
            print("📥 Received response from Gemini API")
            
            # Get the response text
            result = response.text
            
            print(f"📝 Response length: {len(result)} characters")
            print(f"📄 Response preview: {result[:200]}...")
            
            # Parse the result and structure it properly
            try:
                # Try to parse as JSON if the agent returned JSON
                if isinstance(result, str):
                    # Clean up the result string and try to parse as JSON
                    cleaned_result = result.strip()
                    
                    # Remove any markdown formatting if present
                    if cleaned_result.startswith('```json'):
                        cleaned_result = cleaned_result[7:]
                    elif cleaned_result.startswith('```'):
                        cleaned_result = cleaned_result[3:]
                    if cleaned_result.endswith('```'):
                        cleaned_result = cleaned_result[:-3]
                    
                    # Remove any leading/trailing whitespace again
                    cleaned_result = cleaned_result.strip()
                    
                    print("🔍 Attempting to parse JSON response...")
                    print(f"📄 Cleaned response preview: {cleaned_result[:300]}...")
                    
                    parsed_data = json.loads(cleaned_result)
                    print("✅ Successfully parsed JSON response")
                    
                    # Since we enforced a specific schema, the response should be structured correctly
                    # No need to check for nested project_plan structure
                    plan = parsed_data
                    
                    # Validate that all required sections are present
                    required_sections = [
                        'project_overview', 
                        'technical_requirements', 
                        'project_structure', 
                        'file_breakdown', 
                        'implementation_strategy'
                    ]
                    
                    missing_sections = [section for section in required_sections if section not in plan]
                    if missing_sections:
                        print(f"⚠️  Warning: Missing sections in response: {missing_sections}")
                        
                    # Special validation for file_breakdown since it's often missing
                    if 'file_breakdown' not in plan or not plan['file_breakdown'] or plan['file_breakdown'].strip() == '':
                        print("❌ Critical: file_breakdown is missing or empty!")
                        plan['file_breakdown'] = "Error: File breakdown was not generated. Please try again."
                    
                    # Special validation for GUI framework
                    if 'technical_requirements' in plan:
                        tech_req = plan['technical_requirements']
                        if isinstance(tech_req, dict):
                            if not tech_req.get('gui_framework') or tech_req.get('gui_framework').strip() == '':
                                print("⚠️  Warning: GUI framework not specified, setting to 'None'")
                                tech_req['gui_framework'] = 'None'
                                tech_req['gui_framework_justification'] = 'No GUI framework specified by the planning agent'
                        
                else:
                    plan = result
            except json.JSONDecodeError as json_error:
                print(f"❌ JSON parsing failed: {str(json_error)}")
                print(f"📄 Raw response that failed to parse: {result[:500]}...")
                
                # If not valid JSON, structure the text response
                plan = {
                    "project_overview": {
                        "description": "Project plan generated successfully",
                        "status": "completed"
                    },
                    "raw_plan": str(result),
                    "format": "text"
                }
                print("🔄 Converted to text format response")
            
            print(f"📦 Final plan keys: {list(plan.keys()) if isinstance(plan, dict) else 'Not a dict'}")
            return plan
            
        except Exception as e:
            # Return a structured error response
            return {
                "error": True,
                "message": f"Failed to generate project plan: {str(e)}",
                "project_overview": {
                    "description": "Error occurred during plan generation",
                    "status": "failed"
                },
                "raw_plan": f"Error: {str(e)}",
                "format": "error"
            }
