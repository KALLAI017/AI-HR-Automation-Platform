"""
AI Code Analyzer - Uses Groq LLM to evaluate code quality and complexity
"""
import os
from groq import Groq
from dotenv import load_dotenv
import json
from typing import Dict

load_dotenv()


class AICodeAnalyzer:
    """
    Analyzes code using Groq LLM for:
    - Code quality (naming, readability, modularity)
    - Time & space complexity
    - Optimization suggestions
    - Best practices
    """
    
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    
    def analyze_code(self, code: str, language: str, problem_description: str = "") -> Dict:
        """
        Comprehensive code analysis
        
        Args:
            code: Source code to analyze
            language: Programming language
            problem_description: The problem being solved
            
        Returns:
            Dict with quality score, complexity, suggestions
        """
        prompt = f"""You are an expert code reviewer analyzing a {language} solution.

Problem: {problem_description if problem_description else "Not provided"}

Code:
```{language}
{code}
```

Analyze this code and provide a detailed evaluation in JSON format:

{{
  "code_quality_score": <0-100>,
  "quality_breakdown": {{
    "naming_conventions": <0-100>,
    "readability": <0-100>,
    "modularity": <0-100>,
    "comments": <0-100>
  }},
  "time_complexity": "<Big-O notation>",
  "space_complexity": "<Big-O notation>",
  "strengths": ["<strength 1>", "<strength 2>", ...],
  "weaknesses": ["<weakness 1>", "<weakness 2>", ...],
  "optimization_suggestions": ["<suggestion 1>", "<suggestion 2>", ...],
  "best_practices_score": <0-100>,
  "overall_feedback": "<2-3 sentence summary>"
}}

Be precise and constructive. Focus on practical improvements."""

        try:
            response = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert programming interviewer. Provide accurate, helpful code analysis in valid JSON format only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                max_tokens=1500
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Clean JSON from markdown
            if response_text.startswith('```'):
                lines = response_text.split('\n')
                response_text = '\n'.join(lines[1:-1])
                if response_text.startswith('json'):
                    response_text = response_text[4:].strip()
            
            result = json.loads(response_text)
            result['status'] = 'success'
            return result
            
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            print(f"Response: {response_text[:200]}")
            return self._fallback_response(f"Failed to parse AI response: {str(e)}")
        except Exception as e:
            print(f"Analysis error: {e}")
            return self._fallback_response(str(e))
    
    def ask_followup_question(self, code: str, language: str, context: str = "") -> str:
        """
        AI interviewer asks a follow-up question about the code
        
        Args:
            code: The candidate's code
            language: Programming language
            context: Previous conversation context
            
        Returns:
            Follow-up question string
        """
        prompt = f"""You are conducting a technical interview. The candidate wrote this {language} code:

```{language}
{code}
```

{context}

Ask ONE thoughtful follow-up question to assess their understanding. Choose from:
1. "Can you explain your approach and why you chose this solution?"
2. "What is the time and space complexity of your solution?"
3. "Can you optimize this further? What trade-offs would you consider?"
4. "What edge cases did you handle? Are there any you missed?"
5. "How would this scale with very large inputs?"

Return only the question, no extra text."""

        try:
            response = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an experienced technical interviewer. Ask clear, relevant questions."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.5,
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return "Can you explain the time complexity of your solution?"
    
    def evaluate_explanation(self, question: str, answer: str, code: str) -> Dict:
        """
        Evaluate candidate's explanation
        
        Args:
            question: The question asked
            answer: Candidate's answer
            code: Their code
            
        Returns:
            Dict with score and feedback
        """
        prompt = f"""Evaluate this technical interview response:

Question: {question}

Candidate's Answer: {answer}

Their Code:
```
{code}
```

Rate the answer on:
1. Technical accuracy (0-100)
2. Clarity of explanation (0-100)
3. Depth of understanding (0-100)

Provide JSON:
{{
  "accuracy_score": <0-100>,
  "clarity_score": <0-100>,
  "depth_score": <0-100>,
  "overall_score": <0-100>,
  "feedback": "<brief feedback on their answer>"
}}"""

        try:
            response = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are evaluating a technical interview response. Be fair and constructive."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                max_tokens=400
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Clean JSON
            if response_text.startswith('```'):
                lines = response_text.split('\n')
                response_text = '\n'.join(lines[1:-1])
                if response_text.startswith('json'):
                    response_text = response_text[4:].strip()
            
            result = json.loads(response_text)
            result['status'] = 'success'
            return result
            
        except Exception as e:
            return {
                'status': 'error',
                'accuracy_score': 50,
                'clarity_score': 50,
                'depth_score': 50,
                'overall_score': 50,
                'feedback': 'Could not evaluate response'
            }
    
    def _fallback_response(self, error_msg: str) -> Dict:
        """Fallback response when AI analysis fails"""
        return {
            'status': 'error',
            'error': error_msg,
            'code_quality_score': 50,
            'quality_breakdown': {
                'naming_conventions': 50,
                'readability': 50,
                'modularity': 50,
                'comments': 50
            },
            'time_complexity': 'Unable to analyze',
            'space_complexity': 'Unable to analyze',
            'strengths': [],
            'weaknesses': [],
            'optimization_suggestions': [],
            'best_practices_score': 50,
            'overall_feedback': 'AI analysis failed. Manual review recommended.'
        }


# Test function
def test_analyzer():
    """Quick test of AI analyzer"""
    analyzer = AICodeAnalyzer()
    
    test_code = """
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
"""
    
    result = analyzer.analyze_code(
        test_code, 
        'python', 
        'Find two numbers in array that sum to target'
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    test_analyzer()
