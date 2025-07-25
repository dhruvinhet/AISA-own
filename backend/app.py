from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from agents.planning_agent import PlanningAgent

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize the planning agent with error handling
try:
    planning_agent = PlanningAgent()
    print("✅ Planning Agent initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize Planning Agent: {str(e)}")
    print("Please check your environment configuration:")
    print("1. Ensure AI_STUDIO_API_KEY is set in your .env file")
    print("2. Run 'python test_api.py' to verify your setup")
    planning_agent = None

@app.route('/api/plan', methods=['POST'])
def create_plan():
    """
    Endpoint to create a project plan based on user prompt
    """
    try:
        # Check if planning agent is initialized
        if planning_agent is None:
            print("❌ Planning Agent not initialized")
            return jsonify({
                'success': False,
                'error': 'Planning Agent not initialized. Please check server logs and environment configuration.'
            }), 500
        
        data = request.get_json()
        user_prompt = data.get('prompt', '')
        
        print(f"📝 Received request with prompt: {user_prompt[:100]}...")
        
        if not user_prompt:
            print("❌ No prompt provided")
            return jsonify({'error': 'Prompt is required'}), 400
        
        print("🤖 Generating plan with Planning Agent...")
        
        # Generate plan using the planning agent
        plan = planning_agent.create_project_plan(user_prompt)
        
        print(f"✅ Plan generated successfully. Keys: {list(plan.keys())}")
        
        # Check if there was an error in plan generation
        if plan.get('error'):
            print(f"❌ Error in plan generation: {plan.get('message')}")
            return jsonify({
                'success': False,
                'error': plan.get('message', 'Unknown error occurred during plan generation')
            }), 500
        
        response_data = {
            'success': True,
            'plan': plan
        }
        
        print(f"📤 Sending response with success: {response_data['success']}")
        return jsonify(response_data)
    
    except Exception as e:
        print(f"❌ Server error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'message': 'AI Python Code Generator Backend is running',
        'planning_agent_initialized': planning_agent is not None
    })

@app.route('/api/test', methods=['POST'])
def test_endpoint():
    """
    Simple test endpoint to verify API connectivity
    """
    try:
        data = request.get_json()
        test_message = data.get('message', 'No message provided')
        
        print(f"🧪 Test endpoint received: {test_message}")
        
        return jsonify({
            'success': True,
            'echo': test_message,
            'timestamp': str(os.environ.get('TIMESTAMP', 'unknown')),
            'planning_agent_status': 'initialized' if planning_agent else 'not_initialized'
        })
    except Exception as e:
        print(f"❌ Test endpoint error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
