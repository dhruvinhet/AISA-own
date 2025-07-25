import React, { useState } from 'react';
import axios from 'axios';
import { Send, Code, FileText, Folder, Loader2 } from 'lucide-react';
import PlanDisplay from './components/PlanDisplay';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

function App() {
  const [prompt, setPrompt] = useState('');
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!prompt.trim()) {
      setError('Please enter a project description');
      return;
    }

    console.log('🚀 Starting plan generation...');
    setLoading(true);
    setError('');
    setPlan(null);

    try {
      console.log(`📤 Sending request to: ${API_BASE_URL}/api/plan`);
      console.log(`📝 Prompt: ${prompt.substring(0, 100)}...`);
      
      const response = await axios.post(`${API_BASE_URL}/api/plan`, {
        prompt: prompt.trim()
      });

      console.log('📥 Received response:', response);
      console.log('📊 Response status:', response.status);
      console.log('📋 Response data:', response.data);

      if (response.data.success) {
        console.log('✅ Plan generation successful');
        console.log('📦 Plan data:', response.data.plan);
        setPlan(response.data.plan);
      } else {
        console.log('❌ Plan generation failed:', response.data.error);
        setError(response.data.error || 'Failed to generate plan');
      }
    } catch (err) {
      console.error('❌ Error generating plan:', err);
      console.error('📄 Error response:', err.response);
      setError(
        err.response?.data?.error || 
        'Failed to connect to the backend. Please make sure the backend server is running.'
      );
    } finally {
      setLoading(false);
      console.log('🏁 Plan generation process completed');
    }
  };

  const handleClearPlan = () => {
    setPlan(null);
    setError('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Code className="h-10 w-10 text-indigo-600 mr-3" />
            <h1 className="text-4xl font-bold text-gray-900">
              AI Python Code Generator
            </h1>
          </div>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Describe your Python project in natural language, and our AI agents will create a comprehensive project plan for you.
          </p>
        </div>

        {/* Input Form */}
        <div className="max-w-4xl mx-auto mb-8">
          <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-6">
            <div className="mb-4">
              <label htmlFor="prompt" className="block text-sm font-medium text-gray-700 mb-2">
                Project Description
              </label>
              <textarea
                id="prompt"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Describe the Python project you want to build. For example: 'Create a web scraper that extracts product data from e-commerce websites and stores it in a database with a Streamlit dashboard for visualization.'"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
                rows={4}
                disabled={loading}
              />
            </div>

            {error && (
              <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-600 text-sm">{error}</p>
              </div>
            )}

            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-500">
                <span className="font-medium">Note:</span> This system generates Python-only projects with Streamlit or Tkinter for GUI applications.
              </div>
              
              <div className="flex space-x-3">
                {plan && (
                  <button
                    type="button"
                    onClick={handleClearPlan}
                    className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500"
                    disabled={loading}
                  >
                    Clear Plan
                  </button>
                )}
                
                <button
                  type="submit"
                  disabled={loading || !prompt.trim()}
                  className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                >
                  {loading ? (
                    <>
                      <Loader2 className="animate-spin h-4 w-4 mr-2" />
                      Generating Plan...
                    </>
                  ) : (
                    <>
                      <Send className="h-4 w-4 mr-2" />
                      Generate Plan
                    </>
                  )}
                </button>
              </div>
            </div>
          </form>
        </div>

        {/* Plan Display */}
        {plan && (
          <div className="max-w-6xl mx-auto">
            <PlanDisplay plan={plan} />
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-8">
            <div className="flex items-center justify-center">
              <Loader2 className="animate-spin h-8 w-8 text-indigo-600 mr-3" />
              <div>
                <p className="text-lg font-medium text-gray-900">
                  AI Planning Agent is working...
                </p>
                <p className="text-sm text-gray-600">
                  Analyzing your requirements and creating a comprehensive project plan
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-12 text-gray-500 text-sm">
          <p>Powered by CrewAI, Google AI Studio (Gemini 2.5 Flash), and React</p>
          <p className="mt-2">
            <a href="/test" className="text-indigo-600 hover:text-indigo-800 underline">
              Test Plan Display
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
