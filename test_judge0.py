"""
Test Judge0 API to verify it's working correctly
"""
import requests
import base64
import time
import json

def test_judge0_api():
    """Test Judge0 free public instance"""
    
    # Simple Python code that should output "0 1"
    test_code = """nums = [2, 7, 11, 15]
target = 9

seen = {}
for i, num in enumerate(nums):
    diff = target - num
    if diff in seen:
        print(seen[diff], i)
        break
    seen[num] = i
"""
    
    # Encode to base64
    code_b64 = base64.b64encode(test_code.encode()).decode()
    
    # Submission data
    submission = {
        "language_id": 71,  # Python 3
        "source_code": code_b64,
        "stdin": "",
    }
    
    print("Testing Judge0 Free Public Instance...")
    print("=" * 50)
    
    # Submit code
    try:
        response = requests.post(
            "https://ce.judge0.com/submissions?base64_encoded=true&wait=false",
            json=submission,
            headers={"content-type": "application/json"}
        )
        
        print(f"Submit Status: {response.status_code}")
        
        if response.status_code != 201:
            print(f"ERROR: {response.text}")
            return False
        
        token = response.json()['token']
        print(f"Submission Token: {token}")
        
        # Poll for result
        for i in range(10):
            time.sleep(1)
            result_response = requests.get(
                f"https://ce.judge0.com/submissions/{token}?base64_encoded=true",
                headers={"content-type": "application/json"}
            )
            
            if result_response.status_code == 200:
                result = result_response.json()
                status_id = result.get('status', {}).get('id')
                
                print(f"Attempt {i+1}: Status ID = {status_id}")
                
                if status_id not in [1, 2]:  # Not queued or processing
                    # Decode output
                    stdout = base64.b64decode(result.get('stdout', '') or '').decode('utf-8', errors='ignore')
                    stderr = base64.b64decode(result.get('stderr', '') or '').decode('utf-8', errors='ignore')
                    
                    print("\n" + "=" * 50)
                    print("RESULT:")
                    print(f"Status: {result.get('status', {}).get('description', 'Unknown')}")
                    print(f"Output: '{stdout.strip()}'")
                    if stderr:
                        print(f"Error: '{stderr.strip()}'")
                    print(f"Time: {result.get('time', 'N/A')}s")
                    print(f"Memory: {result.get('memory', 'N/A')} KB")
                    print("=" * 50)
                    
                    # Test with actual Two Sum input
                    print("\n\nTesting with Two Sum input...")
                    test_two_sum()
                    
                    return True
        
        print("Timeout waiting for result")
        return False
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False


def test_two_sum():
    """Test with actual Two Sum problem format"""
    
    test_code = """# Read input
nums = list(map(int, input().split()))
target = int(input())

# Solution
seen = {}
for i, num in enumerate(nums):
    diff = target - num
    if diff in seen:
        print(seen[diff], i)
        break
    seen[num] = i
"""
    
    # Test case 1: [2, 7, 11, 15], target = 9
    stdin = "2 7 11 15\n9"
    
    code_b64 = base64.b64encode(test_code.encode()).decode()
    stdin_b64 = base64.b64encode(stdin.encode()).decode()
    
    submission = {
        "language_id": 71,
        "source_code": code_b64,
        "stdin": stdin_b64,
    }
    
    print("=" * 50)
    print("Test Input: [2, 7, 11, 15], target = 9")
    print("Expected Output: 0 1")
    
    try:
        response = requests.post(
            "https://ce.judge0.com/submissions?base64_encoded=true&wait=false",
            json=submission,
            headers={"content-type": "application/json"}
        )
        
        if response.status_code != 201:
            print(f"ERROR: {response.text}")
            return
        
        token = response.json()['token']
        
        # Wait for result
        for i in range(10):
            time.sleep(1)
            result_response = requests.get(
                f"https://ce.judge0.com/submissions/{token}?base64_encoded=true",
                headers={"content-type": "application/json"}
            )
            
            if result_response.status_code == 200:
                result = result_response.json()
                status_id = result.get('status', {}).get('id')
                
                if status_id not in [1, 2]:
                    stdout = base64.b64decode(result.get('stdout', '') or '').decode('utf-8', errors='ignore')
                    stderr = base64.b64decode(result.get('stderr', '') or '').decode('utf-8', errors='ignore')
                    
                    print(f"Actual Output: '{stdout.strip()}'")
                    if stderr:
                        print(f"Error: '{stderr.strip()}'")
                    
                    if stdout.strip() == "0 1":
                        print("✅ TEST PASSED!")
                    else:
                        print("❌ TEST FAILED!")
                    print("=" * 50)
                    return
        
    except Exception as e:
        print(f"ERROR: {str(e)}")


if __name__ == "__main__":
    test_judge0_api()
