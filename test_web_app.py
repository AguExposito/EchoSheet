import requests
import json

def test_web_app():
    """Test the web application directly"""
    print("=== Testing Web Application ===")
    
    try:
        # Test the character page
        print("1. Testing character page...")
        response = requests.get('http://localhost:5000/character/20', timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Character page loaded successfully")
            
            # Check if spells are in the HTML
            html = response.text
            if "Acid Splash" in html or "Burning Hands" in html:
                print("✅ Spells found in HTML")
            else:
                print("❌ Spells not found in HTML")
                
            if "No Spells Available" in html:
                print("⚠️  'No Spells Available' message found")
            else:
                print("✅ No 'No Spells Available' message")
                
        else:
            print(f"❌ Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - app may not be running")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_web_app() 