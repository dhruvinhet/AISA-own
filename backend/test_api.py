#!/usr/bin/env python3
"""
Test script to verify Google AI Studio API connectivity
"""
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

def test_api_connection():
    """Test the Google AI Studio API connection"""
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('AI_STUDIO_API_KEY')
    
    if not api_key:
        print("❌ Error: AI_STUDIO_API_KEY not found in environment variables")
        print("Please make sure you have:")
        print("1. Created a .env file (copy from .env.example)")
        print("2. Added your Google AI Studio API key")
        print("3. Get your API key from: https://aistudio.google.com/app/apikey")
        return False
    
    if api_key == "your_ai_studio_api_key_here":
        print("❌ Error: Please replace the placeholder API key with your actual key")
        return False
    
    try:
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Test with a simple prompt using the latest model
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content("Say 'Hello, API connection successful!'")
        
        print("✅ API Connection Test Successful!")
        print(f"Response: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ API Connection Test Failed: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Verify your API key is correct")
        print("2. Check that you have internet connectivity") 
        print("3. Ensure your Google AI Studio account has quota available")
        print("4. Visit https://aistudio.google.com/app/apikey to verify your key")
        return False

if __name__ == "__main__":
    print("🧪 Testing Google AI Studio API Connection...")
    print("=" * 50)
    
    success = test_api_connection()
    
    if success:
        print("\n✅ All tests passed! Your setup is ready.")
        print("You can now run the full application with: python app.py")
    else:
        print("\n❌ Setup incomplete. Please fix the issues above.")
        sys.exit(1)
