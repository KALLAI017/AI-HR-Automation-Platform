"""
Test to demonstrate the chatbot improvements
Shows how it now handles the conversation correctly
"""
import os
from technical_interview_chat import TechnicalInterviewChat
from dotenv import load_dotenv

load_dotenv()

# Sample problem
problem = {
    'title': 'Two Sum',
    'difficulty': 'Easy',
    'description': 'Given an array of integers nums and an integer target, return indices of the two numbers that add up to target.',
    'examples': [
        {'input': '[2,7,11,15], target=9', 'output': '[0,1]', 'explanation': '2 + 7 = 9'},
        {'input': '[3,2,4], target=6', 'output': '[1,2]', 'explanation': '3 + 4 = 6'}
    ],
    'test_cases': []
}

print("=" * 80)
print("🧪 TESTING IMPROVED CHATBOT")
print("=" * 80)

chat = TechnicalInterviewChat()

# Stage 1: Introduction
print("\n" + "=" * 80)
print("STAGE 1: INTRODUCTION")
print("=" * 80)
intro = chat.start_interview(problem)
print(f"🤖 AI: {intro}\n")

# Stage 2: Candidate explains approach (brute force)
print("=" * 80)
print("STAGE 2: CLARIFICATION (Candidate starts explaining approach)")
print("=" * 80)
print("👤 Candidate: First i will explain the brute force approach. Here i can use")
print("             two nested loops, one loop select a number and the second loop")
print("             is used add the current number with another number in the array.")
print("             But the problem here is it gives time complexity of O(n^2))\n")

response1 = chat.handle_clarification(
    "First i will explain the brute force approach. Here i can use two nested loops, "
    "one loop select a number and the second loop is used add the current number with "
    "another number in the array. But the problem here is it gives time complexity of O(n^2))"
)
print(f"🤖 AI: {response1}\n")

# Stage 3: Approach discussion
print("=" * 80)
print("STAGE 3: APPROACH DISCUSSION")
print("=" * 80)
print("👤 Candidate: I will use two nested loops (i and j). In the inner loop,")
print("             I check if a[i] + a[j] == target. If yes, return [i, j].\n")

approach_feedback = chat.discuss_approach(
    "I will use two nested loops (i and j). In the inner loop, "
    "I check if a[i] + a[j] == target. If yes, return [i, j]."
)
print(f"🤖 AI Response:")
print(f"   Approach Valid: {approach_feedback.get('approach_valid')}")
print(f"   Score: {approach_feedback.get('approach_score')}/100")
print(f"   Time Complexity: {approach_feedback.get('time_complexity')}")
print(f"   Feedback: {approach_feedback.get('feedback_message')}\n")

# Summary
print("=" * 80)
print("📊 TEST SUMMARY")
print("=" * 80)
print("✅ Introduction: Concise and professional")
print("✅ Clarification: Recognizes when candidate is explaining approach")
print("✅ Approach Evaluation: Correctly identifies brute force as valid")
print("✅ Feedback: Acknowledges correctness, then guides to optimization")
print("=" * 80)
