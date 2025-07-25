#!/usr/bin/env python3
"""
Test script to verify the API endpoints are working
"""
import requests
import json
import sys

def test_backend():
    """Test the backend API endpoints"""
    
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Backend API Endpoints")
    print("=" * 50)
    
    # Test health endpoint
    try:
        print("1. Testing health endpoint...")
        response = requests.get(f"{base_url}/api/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print()
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
        return False
    
    # Test simple echo endpoint
    try:
        print("2. Testing echo endpoint...")
        test_data = {"message": "Hello from test script"}
        response = requests.post(f"{base_url}/api/test", json=test_data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print()
    except Exception as e:
        print(f"   ❌ Echo test failed: {e}")
        return False
    
    # Test plan generation with a simple prompt
    try:
        print("3. Testing plan generation...")
        plan_data = {"prompt": "Create a simple calculator app"}
        response = requests.post(f"{base_url}/api/plan", json=plan_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Success: {result.get('success')}")
            if result.get('success'):
                plan = result.get('plan', {})
                print(f"   Plan keys: {list(plan.keys())}")
                
                # Print the actual plan structure for debugging
                print(f"   Full plan structure:")
                
                # Print each section separately for better readability
                for key, value in plan.items():
                    print(f"\n   === {key.upper()} ===")
                    if isinstance(value, dict):
                        for subkey, subvalue in value.items():
                            print(f"     {subkey}: {str(subvalue)[:100]}{'...' if len(str(subvalue)) > 100 else ''}")
                    elif isinstance(value, list):
                        print(f"     [Array with {len(value)} items]")
                        if value:
                            print(f"     First item: {str(value[0])[:100]}{'...' if len(str(value[0])) > 100 else ''}")
                    else:
                        print(f"     {str(value)[:100]}{'...' if len(str(value)) > 100 else ''}")
                
                if 'raw_plan' in plan:
                    print(f"   Raw plan preview: {plan['raw_plan'][:200]}...")
                else:
                    print(f"   Structured plan with {len(plan)} sections")
            else:
                print(f"   Error: {result.get('error')}")
        else:
            print(f"   ❌ Failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
        
        print()
        return True
        
    except Exception as e:
        print(f"   ❌ Plan generation test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting backend API tests...")
    print("Make sure the backend server is running on localhost:5000")
    print()
    
    try:
        success = test_backend()
        if success:
            print("✅ All tests completed! Check the output above for details.")
        else:
            print("❌ Some tests failed. Check the backend server logs.")
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
