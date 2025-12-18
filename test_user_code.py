"""
Test the exact code from the user
"""
from code_executor import CodeExecutor

executor = CodeExecutor()

# User's code that always returns 0, 1
user_code = """# Read input
nums = list(map(int, input().split()))
target = int(input())

# Your solution here
def two_sum(nums, target):
    return 0 ,1

# Call function and print result
result = two_sum(nums, target)
if result:
    print(result[0], result[1])
"""

# Test cases
test_cases = [
    {"input": "2 7 11 15\n9", "expected": "0 1", "visible": True},
    {"input": "3 2 4\n6", "expected": "1 2", "visible": True},
]

print("Testing user's code (always returns 0, 1):")
print("=" * 60)
results = executor.run_test_cases(user_code, 'python', test_cases)
print(f"Total: {results['total']}")
print(f"Passed: {results['passed']}")
print(f"Failed: {results['failed']}")
print()

for test in results['test_results']:
    status_icon = "✅" if test['status'] == 'passed' else "❌"
    print(f"{status_icon} Test {test['test_number']}: {test['status'].upper()}")
    print(f"   Input: {test['input']}")
    print(f"   Expected: '{test['expected']}'")
    print(f"   Got: '{test['actual']}'")
    print()

if results['passed'] == 1 and results['failed'] == 1:
    print("✅ CORRECT BEHAVIOR - Test 1 passed, Test 2 failed")
else:
    print(f"❌ WRONG BEHAVIOR - Both tests passed when Test 2 should fail!")
