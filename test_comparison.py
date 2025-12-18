"""
Test the comparison logic
"""
from code_executor import CodeExecutor

executor = CodeExecutor()

# Test cases
test_cases = [
    ("0 1", "0 1", True),      # Exact match
    ("0 1", "1 2", False),     # Different values
    ("[0, 1]", "0 1", True),   # Normalized match
    ("0 1", "1 0", False),     # Wrong order
    ("  0   1  ", "0 1", True), # Whitespace
]

print("Testing _compare_outputs method:")
print("=" * 60)

for actual, expected, should_match in test_cases:
    result = executor._compare_outputs(actual, expected)
    status = "✅" if result == should_match else "❌"
    print(f"{status} '{actual}' vs '{expected}' -> {result} (expected {should_match})")

print("=" * 60)
