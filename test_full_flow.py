"""
Test the full run_test_cases flow
"""
from code_executor import CodeExecutor

executor = CodeExecutor()

# Correct code
correct_code = """# Read input
nums = list(map(int, input().split()))
target = int(input())

seen = {}
for i, num in enumerate(nums):
    diff = target - num
    if diff in seen:
        print(seen[diff], i)
        break
    seen[num] = i
"""

# Wrong code
wrong_code = """# Read input
nums = list(map(int, input().split()))
target = int(input())

# Always outputs 1 2 (wrong)
print(1, 2)
"""

# Test cases
test_cases = [
    {"input": "2 7 11 15\n9", "expected": "0 1", "visible": True},
    {"input": "3 2 4\n6", "expected": "1 2", "visible": True},
]

print("Testing CORRECT code:")
print("=" * 60)
results_correct = executor.run_test_cases(correct_code, 'python', test_cases)
print(f"Total: {results_correct['total']}")
print(f"Passed: {results_correct['passed']}")
print(f"Failed: {results_correct['failed']}")
for test in results_correct['test_results']:
    print(f"  Test {test['test_number']}: {test['status']} - Expected: '{test['expected']}' Got: '{test['actual']}'")

print("\n" + "=" * 60)
print("Testing WRONG code:")
print("=" * 60)
results_wrong = executor.run_test_cases(wrong_code, 'python', test_cases)
print(f"Total: {results_wrong['total']}")
print(f"Passed: {results_wrong['passed']}")
print(f"Failed: {results_wrong['failed']}")
for test in results_wrong['test_results']:
    print(f"  Test {test['test_number']}: {test['status']} - Expected: '{test['expected']}' Got: '{test['actual']}'")

print("\n" + "=" * 60)
if results_correct['passed'] == 2 and results_wrong['passed'] == 0:
    print("✅ ALL TESTS WORKING CORRECTLY!")
else:
    print("❌ PROBLEM DETECTED!")
    print(f"Correct code should pass 2/2, got {results_correct['passed']}/2")
    print(f"Wrong code should pass 0/2, got {results_wrong['passed']}/2")
