"""
Simple test script to verify the authentication API is working.
Run this after starting the API server.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("Testing Authentication API...")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print("❌ Health check failed")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running.")
        return
    
    # Test 2: Sign up
    print("\n2. Testing user signup...")
    signup_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/signup", json=signup_data)
        if response.status_code == 200:
            print("✅ User signup successful")
        elif response.status_code == 400 and "already registered" in response.text:
            print("ℹ️  User already exists (this is expected if you've run this test before)")
        else:
            print(f"❌ Signup failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Signup error: {e}")
        return
    
    # Test 3: Sign in
    print("\n3. Testing user signin...")
    signin_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/signin", json=signin_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print("✅ User signin successful")
            print(f"   Token received: {token[:20]}...")
            
            # Test 4: Protected endpoint
            print("\n4. Testing protected endpoint...")
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
            
            if response.status_code == 200:
                user_data = response.json()
                print("✅ Protected endpoint access successful")
                print(f"   User: {user_data.get('first_name')} {user_data.get('last_name')}")
            else:
                print(f"❌ Protected endpoint failed: {response.text}")
        else:
            print(f"❌ Signin failed: {response.text}")
    except Exception as e:
        print(f"❌ Signin error: {e}")
    
    # Test 5: Forgot password
    print("\n5. Testing forgot password...")
    forgot_data = {"email": "test@example.com"}
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/forgot-password", json=forgot_data)
        if response.status_code == 200:
            print("✅ Forgot password endpoint working")
            print("   (Email sending may fail if SMTP is not configured)")
        else:
            print(f"❌ Forgot password failed: {response.text}")
    except Exception as e:
        print(f"❌ Forgot password error: {e}")
    
    print("\n" + "=" * 50)
    print("API Testing Complete!")
    print("\nNext steps:")
    print("1. Configure your .env file with real Supabase credentials")
    print("2. Set up SMTP for email functionality")
    print("3. Connect your React frontend to these endpoints")

if __name__ == "__main__":
    test_api()
