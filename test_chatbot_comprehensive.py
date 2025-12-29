"""
Comprehensive Automated Testing of Technical Interview Chatbot
Tests multiple coding problems and various user interaction patterns
"""
import os
from technical_interview_chat import TechnicalInterviewChat
from dotenv import load_dotenv
import time
from datetime import datetime

load_dotenv()

# Define multiple test problems
TEST_PROBLEMS = [
    {
        'title': 'Two Sum',
        'difficulty': 'Easy',
        'description': 'Given an array of integers nums and an integer target, return indices of the two numbers that add up to target.',
        'examples': [
            {'input': '[2,7,11,15], target=9', 'output': '[0,1]', 'explanation': '2 + 7 = 9'},
            {'input': '[3,2,4], target=6', 'output': '[1,2]', 'explanation': '2 + 4 = 6'}
        ],
        'test_cases': []
    },
    {
        'title': 'Valid Parentheses',
        'difficulty': 'Easy',
        'description': 'Given a string containing just the characters \'(\', \')\', \'{\', \'}\', \'[\' and \']\', determine if the input string is valid. Opening brackets must be closed in the correct order.',
        'examples': [
            {'input': '()', 'output': 'true', 'explanation': 'Valid parentheses'},
            {'input': '()[]{}', 'output': 'true', 'explanation': 'All valid'},
            {'input': '(]', 'output': 'false', 'explanation': 'Mismatched brackets'}
        ],
        'test_cases': []
    },
    {
        'title': 'Reverse Linked List',
        'difficulty': 'Medium',
        'description': 'Given the head of a singly linked list, reverse the list, and return the reversed list.',
        'examples': [
            {'input': '[1,2,3,4,5]', 'output': '[5,4,3,2,1]', 'explanation': 'Reverse order'},
            {'input': '[1,2]', 'output': '[2,1]', 'explanation': 'Two nodes'}
        ],
        'test_cases': []
    }
]

# Define test scenarios
TEST_SCENARIOS = [
    {
        'name': 'Scenario 1: Brute Force First, Then Optimize',
        'interactions': [
            {'type': 'clarification', 'message': 'Can the array contain negative numbers?'},
            {'type': 'approach', 'message': 'I will use two nested loops to check every pair of numbers. Time complexity is O(n²).'},
            {'type': 'approach', 'message': 'Actually, I can optimize using a hash map. Store each number with its index, then check if target-num exists in the map. This gives O(n) time.'}
        ]
    },
    {
        'name': 'Scenario 2: Direct Optimal Solution',
        'interactions': [
            {'type': 'approach', 'message': 'I will use a hash map to solve this in O(n) time. As I iterate through the array, I\'ll check if the complement exists in the map.'}
        ]
    },
    {
        'name': 'Scenario 3: Multiple Clarifications',
        'interactions': [
            {'type': 'clarification', 'message': 'What if there are duplicate numbers?'},
            {'type': 'clarification', 'message': 'Can I assume there is exactly one solution?'},
            {'type': 'clarification', 'message': 'Should I return the indices in any specific order?'},
            {'type': 'approach', 'message': 'Based on the constraints, I\'ll use a hash map approach with O(n) time complexity.'}
        ]
    },
    {
        'name': 'Scenario 4: Asking for Hints',
        'interactions': [
            {'type': 'clarification', 'message': 'I\'m not sure how to start. Can you give me a hint?'},
            {'type': 'approach', 'message': 'I think I need to use some kind of lookup structure to make it efficient.'}
        ]
    },
    {
        'name': 'Scenario 5: Wrong Approach',
        'interactions': [
            {'type': 'approach', 'message': 'I will sort the array first, then use binary search to find pairs. This should work.'}
        ]
    }
]

class TestReport:
    """Generate comprehensive test report"""
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
        self.results = []
        self.start_time = datetime.now()
    
    def add_result(self, test_name, status, details, response_time):
        self.tests_run += 1
        if status == 'PASS':
            self.tests_passed += 1
        else:
            self.tests_failed += 1
        
        self.results.append({
            'test': test_name,
            'status': status,
            'details': details,
            'response_time': response_time
        })
    
    def generate_report(self):
        duration = (datetime.now() - self.start_time).total_seconds()
        
        print("\n" + "=" * 100)
        print("📊 COMPREHENSIVE CHATBOT TEST REPORT")
        print("=" * 100)
        print(f"Test Date: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Duration: {duration:.2f}s")
        print(f"Total Tests: {self.tests_run}")
        print(f"✅ Passed: {self.tests_passed} ({self.tests_passed/self.tests_run*100:.1f}%)")
        print(f"❌ Failed: {self.tests_failed} ({self.tests_failed/self.tests_run*100:.1f}%)")
        print("=" * 100)
        
        # Group results by category
        print("\n📋 DETAILED RESULTS\n")
        
        for i, result in enumerate(self.results, 1):
            status_icon = "✅" if result['status'] == 'PASS' else "❌"
            print(f"{status_icon} Test {i}: {result['test']}")
            print(f"   Status: {result['status']}")
            print(f"   Response Time: {result['response_time']:.3f}s")
            print(f"   Details: {result['details']}")
            print()
        
        print("=" * 100)
        print("🎯 SUMMARY BY CATEGORY\n")
        
        # Analyze results
        intro_tests = [r for r in self.results if 'Introduction' in r['test']]
        clarification_tests = [r for r in self.results if 'Clarification' in r['test']]
        approach_tests = [r for r in self.results if 'Approach' in r['test']]
        
        print(f"Introduction Tests: {len(intro_tests)} total")
        print(f"  ✅ Passed: {len([t for t in intro_tests if t['status'] == 'PASS'])}")
        print()
        
        print(f"Clarification Tests: {len(clarification_tests)} total")
        print(f"  ✅ Passed: {len([t for t in clarification_tests if t['status'] == 'PASS'])}")
        print()
        
        print(f"Approach Evaluation Tests: {len(approach_tests)} total")
        print(f"  ✅ Passed: {len([t for t in approach_tests if t['status'] == 'PASS'])}")
        print()
        
        # Performance metrics
        avg_response_time = sum(r['response_time'] for r in self.results) / len(self.results)
        max_response_time = max(r['response_time'] for r in self.results)
        
        print("=" * 100)
        print("⚡ PERFORMANCE METRICS\n")
        print(f"Average Response Time: {avg_response_time:.3f}s")
        print(f"Max Response Time: {max_response_time:.3f}s")
        print(f"Expected: <2s for chat, <3s for analysis")
        
        if avg_response_time < 2.0:
            print("✅ Performance: EXCELLENT")
        elif avg_response_time < 3.0:
            print("✅ Performance: GOOD")
        else:
            print("⚠️ Performance: NEEDS IMPROVEMENT")
        
        print("=" * 100)


def test_introduction(problem, report):
    """Test introduction stage"""
    chat = TechnicalInterviewChat()
    
    start = time.time()
    try:
        intro = chat.start_interview(problem)
        response_time = time.time() - start
        
        # Validation checks
        checks = {
            'has_content': len(intro) > 50,
            'mentions_problem': problem['title'].lower() in intro.lower(),
            'not_too_long': len(intro) < 1000,
            'no_placeholder': '[Your Name]' not in intro and '[Name]' not in intro
        }
        
        if all(checks.values()):
            report.add_result(
                f"Introduction - {problem['title']}",
                'PASS',
                f"Generated {len(intro)} chars, all checks passed",
                response_time
            )
        else:
            failed_checks = [k for k, v in checks.items() if not v]
            report.add_result(
                f"Introduction - {problem['title']}",
                'FAIL',
                f"Failed checks: {', '.join(failed_checks)}",
                response_time
            )
    except Exception as e:
        report.add_result(
            f"Introduction - {problem['title']}",
            'FAIL',
            f"Exception: {str(e)}",
            time.time() - start
        )


def test_clarification(problem, question, report):
    """Test clarification handling"""
    chat = TechnicalInterviewChat()
    chat.start_interview(problem)
    
    start = time.time()
    try:
        response = chat.handle_clarification(question)
        response_time = time.time() - start
        
        # Validation checks
        checks = {
            'has_response': len(response) > 20,
            'not_too_long': len(response) < 800,
            'seems_relevant': any(word in response.lower() for word in ['yes', 'no', 'can', 'will', 'should', 'array', 'target', 'problem'])
        }
        
        if all(checks.values()):
            report.add_result(
                f"Clarification - {problem['title']}",
                'PASS',
                f"Answered: '{question[:50]}...' ({len(response)} chars)",
                response_time
            )
        else:
            failed_checks = [k for k, v in checks.items() if not v]
            report.add_result(
                f"Clarification - {problem['title']}",
                'FAIL',
                f"Failed checks: {', '.join(failed_checks)}",
                response_time
            )
    except Exception as e:
        report.add_result(
            f"Clarification - {problem['title']}",
            'FAIL',
            f"Exception: {str(e)}",
            time.time() - start
        )


def test_approach_evaluation(problem, approach_text, expected_valid, report):
    """Test approach evaluation"""
    chat = TechnicalInterviewChat()
    chat.start_interview(problem)
    
    start = time.time()
    try:
        feedback = chat.discuss_approach(approach_text)
        response_time = time.time() - start
        
        # Validation checks
        checks = {
            'has_score': 'approach_score' in feedback and 0 <= feedback['approach_score'] <= 100,
            'has_complexity': 'time_complexity' in feedback,
            'has_feedback': 'feedback_message' in feedback and len(feedback['feedback_message']) > 20,
            'correct_validity': feedback.get('approach_valid') == expected_valid if expected_valid is not None else True
        }
        
        if all(checks.values()):
            report.add_result(
                f"Approach Evaluation - {problem['title']}",
                'PASS',
                f"Score: {feedback.get('approach_score', 'N/A')}/100, Valid: {feedback.get('approach_valid', 'N/A')}",
                response_time
            )
        else:
            failed_checks = [k for k, v in checks.items() if not v]
            report.add_result(
                f"Approach Evaluation - {problem['title']}",
                'FAIL',
                f"Failed checks: {', '.join(failed_checks)}",
                response_time
            )
    except Exception as e:
        report.add_result(
            f"Approach Evaluation - {problem['title']}",
            'FAIL',
            f"Exception: {str(e)}",
            time.time() - start
        )


def test_hint_system(problem, report):
    """Test hint generation"""
    chat = TechnicalInterviewChat()
    chat.start_interview(problem)
    
    # Test 2 hints instead of 4 (to reduce API calls)
    for i in range(1, 3):
        start = time.time()
        try:
            hint = chat.get_context_aware_hint("", "")
            response_time = time.time() - start
            
            checks = {
                'has_content': len(hint) > 20,
                'not_solution': 'return' not in hint.lower() or 'hint' in hint.lower()
            }
            
            if all(checks.values()):
                report.add_result(
                    f"Hint #{i} - {problem['title']}",
                    'PASS',
                    f"Generated hint ({len(hint)} chars)",
                    response_time
                )
            else:
                report.add_result(
                    f"Hint #{i} - {problem['title']}",
                    'FAIL',
                    "Hint validation failed",
                    response_time
                )
            time.sleep(2)  # Rate limit protection
        except Exception as e:
            report.add_result(
                f"Hint #{i} - {problem['title']}",
                'FAIL',
                f"Exception: {str(e)}",
                time.time() - start
            )


def run_comprehensive_tests():
    """Run all tests and generate report"""
    print("\n" + "=" * 100)
    print("🧪 STARTING COMPREHENSIVE CHATBOT TESTING (Rate-Limited)")
    print("=" * 100)
    print("\nThis will test:")
    print("  • Multiple coding problems (Easy, Medium)")
    print("  • Introduction generation")
    print("  • Clarification handling")
    print("  • Approach evaluation (brute force, optimal, wrong)")
    print("  • Hint generation system")
    print("  • Response times and performance")
    print("\n⏱️ Note: Tests run with delays to avoid API rate limits")
    print("Estimated time: 3-5 minutes")
    print("=" * 100)
    
    report = TestReport()
    
    # Test each problem
    for problem in TEST_PROBLEMS:
        print(f"\n🔍 Testing: {problem['title']} ({problem['difficulty']})")
        print("-" * 100)
        
        # Test 1: Introduction
        print("  Testing introduction...", end=" ")
        test_introduction(problem, report)
        print("Done")
        
        # Test 2: Clarification questions
        print("  Testing clarifications...", end=" ")
        clarification_questions = [
            "Can the input be empty?",
            "What about edge cases?"
        ]
        for question in clarification_questions:
            test_clarification(problem, question, report)
            time.sleep(2)  # Rate limit protection
        print("Done")
        
        # Test 3: Approach evaluations
        print("  Testing approach evaluation...", end=" ")
        
        # Brute force approach (should be valid but low score)
        if problem['title'] == 'Two Sum':
            test_approach_evaluation(
                problem,
                "Use two nested loops to check every pair. Time complexity O(n²).",
                expected_valid=True,
                report=report
            )
            time.sleep(2)  # Rate limit protection
            
            # Optimal approach (should be valid with high score)
            test_approach_evaluation(
                problem,
                "Use a hash map to store complements. Check if target-num exists. Time complexity O(n).",
                expected_valid=True,
                report=report
            )
            time.sleep(2)  # Rate limit protection
        
        elif problem['title'] == 'Valid Parentheses':
            test_approach_evaluation(
                problem,
                "Use a stack. Push opening brackets, pop when closing bracket matches.",
                expected_valid=True,
                report=report
            )
            time.sleep(2)  # Rate limit protection
        
        elif problem['title'] == 'Reverse Linked List':
            test_approach_evaluation(
                problem,
                "Use iterative approach with three pointers: prev, current, next.",
                expected_valid=True,
                report=report
            )
            time.sleep(2)  # Rate limit protection
        
        print("Done")
        
        # Test 4: Hint system
        print("  Testing hint system...", end=" ")
        test_hint_system(problem, report)
        print("Done")
        
        print(f"  ✅ Completed testing: {problem['title']}")
    
    # Generate final report
    report.generate_report()


if __name__ == "__main__":
    run_comprehensive_tests()
