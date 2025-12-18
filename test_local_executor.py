"""
Test local executor to verify it's working correctly
"""
from local_executor import LocalPythonExecutor

def test_correct_code():
    """Test with correct Two Sum solution"""
    executor = LocalPythonExecutor()
    
    code = """# Read input
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
    result = executor.execute_python(code, stdin)
    
    print("Test 1 - Correct Code:")
    print(f"Status: {result['status']}")
    print(f"Output: '{result['output']}'")
    print(f"Expected: '0 1'")
    print(f"Match: {result['output'] == '0 1'}")
    print()

def test_wrong_code():
    """Test with wrong solution"""
    executor = LocalPythonExecutor()
    
    code = """# Read input
nums = list(map(int, input().split()))
target = int(input())

# Wrong solution - always returns 1 2
print(1, 2)
"""
    
    stdin = "2 7 11 15\n9"
    result = executor.execute_python(code, stdin)
    
    print("Test 2 - Wrong Code:")
    print(f"Status: {result['status']}")
    print(f"Output: '{result['output']}'")
    print(f"Expected: '0 1'")
    print(f"Match: {result['output'] == '0 1'}")
    print()

def test_error_code():
    """Test with code that has errors"""
    executor = LocalPythonExecutor()
    
    code = """# Read input
nums = list(map(int, input().split()))
target = int(input())

# Error - undefined variable
print(undefined_variable)
"""
    
    stdin = "2 7 11 15\n9"
    result = executor.execute_python(code, stdin)
    
    print("Test 3 - Error Code:")
    print(f"Status: {result['status']}")
    print(f"Output: '{result['output']}'")
    print(f"Error: '{result['error']}'")
    print()

if __name__ == "__main__":
    test_correct_code()
    test_wrong_code()
    test_error_code()
