"""
Technical Interview Chat System - AI Interviewer with Context-Aware Hints
Uses hybrid LLM approach: llama-3.1-8b-instant for chat, llama-3.3-70b for analysis
"""
import os
from groq import Groq
from dotenv import load_dotenv
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime

load_dotenv()


class TechnicalInterviewChat:
    """
    AI-powered technical interviewer with:
    - Natural conversation flow
    - Context-aware hints
    - Multi-turn debugging
    - Socratic questioning
    - Adaptive difficulty
    """
    
    # Interview stages
    STAGES = {
        'INTRODUCTION': 'introduction',
        'CLARIFICATION': 'clarification',
        'APPROACH': 'approach',
        'CODING': 'coding',
        'REVIEW': 'review',
        'COMPLETE': 'complete'
    }
    
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.chat_model = "llama-3.1-8b-instant"  # Fast for conversation
        self.analysis_model = "llama-3.3-70b-versatile"  # Deep for code analysis
        
        # Interview state
        self.current_stage = self.STAGES['INTRODUCTION']
        self.conversation_history = []
        self.problem_data = {}
        self.hint_count = 0
        self.max_hints = 3
        self.candidate_code = ""
        self.approach_quality = 0
        self.communication_score = 0
        
    def start_interview(self, problem: Dict) -> str:
        """
        Initialize interview with problem introduction
        
        Args:
            problem: Problem data (title, description, examples, etc.)
            
        Returns:
            AI's introduction message
        """
        self.problem_data = problem
        self.current_stage = self.STAGES['INTRODUCTION']
        
        prompt = f"""You are a friendly technical interviewer conducting a coding interview.

**Problem:** {problem['title']} ({problem['difficulty']})

**Description:**
{problem['description']}

**Examples:**
{self._format_examples(problem['examples'])}

Your task:
1. Give a brief, warm greeting (1 sentence)
2. Introduce the problem conversationally (2-3 sentences)
3. Show ONE example to illustrate
4. Ask: "Do you have any clarifying questions before we discuss your approach?"

Be concise (max 5 sentences total). Keep it natural and encouraging."""

        response = self._call_llm(prompt, model=self.chat_model)
        self._add_to_history('assistant', response, 'introduction')
        
        return response
    
    def handle_clarification(self, candidate_question: str) -> str:
        """
        Answer clarification questions about the problem
        
        Args:
            candidate_question: Candidate's question
            
        Returns:
            AI's helpful answer
        """
        self.current_stage = self.STAGES['CLARIFICATION']
        self._add_to_history('user', candidate_question, 'clarification')
        
        prompt = f"""You are a technical interviewer. The candidate said:

"{candidate_question}"

Problem context:
{self._get_problem_context()}

Conversation so far:
{self._get_recent_conversation(5)}

IMPORTANT:
- If they're EXPLAINING their approach (using words like "I will", "my approach", "brute force"), 
  say: "Great! Let me hear your full approach before we dive into coding. Walk me through your solution step by step."
  Then STOP and wait for their complete explanation.
  
- If they're ASKING a question about the problem:
  * Good clarifying question: Praise them and answer clearly
  * Already explained: Gently point to problem statement
  
Keep response SHORT (2-3 sentences max). Don't over-explain."""

        response = self._call_llm(prompt, model=self.chat_model)
        self._add_to_history('assistant', response, 'clarification')
        
        return response
    
    def discuss_approach(self, candidate_explanation: str) -> Dict:
        """
        Evaluate candidate's approach before coding
        
        Args:
            candidate_explanation: How they plan to solve it
            
        Returns:
            Dict with feedback, score, and next steps
        """
        self.current_stage = self.STAGES['APPROACH']
        self._add_to_history('user', candidate_explanation, 'approach')
        
        prompt = f"""You are a technical interviewer evaluating the candidate's approach.

Problem: {self.problem_data['title']}

Candidate's explanation:
"{candidate_explanation}"

Analyze their approach:
1. Is the logic correct? (Will it produce the right answer?)
2. What's the time/space complexity?
3. If it's brute force (O(n²)), acknowledge it's correct but ask about optimization

IMPORTANT:
- For brute force (nested loops): approach_valid=true, score=60-70, then ask "Can we optimize this?"
- For optimal (hash map): approach_valid=true, score=90-100, praise and move to coding
- For incorrect: approach_valid=false, score=30-50, guide with questions

Provide feedback in JSON format:
{{
  "approach_valid": true/false,
  "approach_score": <0-100>,
  "time_complexity": "O(...)",
  "space_complexity": "O(...)",
  "strengths": ["strength1", "strength2"],
  "concerns": ["concern1 if any"],
  "follow_up_question": "Ask about optimization if brute force, or edge cases if optimal",
  "feedback_message": "SHORT response (2-3 sentences). If brute force: say 'Correct! But can we do better than O(n²)?' If optimal: 'Excellent! Let's implement it.'"
}}

Be encouraging. Don't create confusion where there is none."""

        response = self._call_llm(prompt, model=self.analysis_model, json_mode=True)
        
        try:
            feedback = json.loads(response)
            self.approach_quality = feedback.get('approach_score', 50)
            
            # Add feedback to history
            self._add_to_history('assistant', feedback['feedback_message'], 'approach')
            
            return feedback
        except:
            # Fallback if JSON parsing fails
            self._add_to_history('assistant', response, 'approach')
            return {
                'approach_valid': True,
                'approach_score': 70,
                'feedback_message': response
            }
    
    def get_context_aware_hint(self, current_code: str, error_message: str = "") -> str:
        """
        Provide intelligent hints based on code progress
        
        Args:
            current_code: Candidate's current code
            error_message: Any error they're encountering
            
        Returns:
            Helpful hint without giving away solution
        """
        if self.hint_count >= self.max_hints:
            return "You've used all available hints. Try to debug this yourself - you're close!"
        
        self.hint_count += 1
        self.candidate_code = current_code
        
        prompt = f"""You are a helpful coding mentor. The candidate is stuck on this problem:

**Problem:** {self.problem_data['title']}

**Their current code:**
```
{current_code if current_code.strip() else "No code written yet"}
```

**Error (if any):**
{error_message if error_message else "No specific error, just stuck"}

**Hint #{self.hint_count} of {self.max_hints}**

Analyze their code and provide a strategic hint:
- If no code: Suggest a data structure or algorithm pattern
- If partial code: Identify what's working and what's missing
- If error: Guide them toward the bug with a question, don't fix it directly
- If close: Suggest edge cases to consider

Use Socratic questioning. Make them think. Be encouraging.
Keep hint under 3 sentences."""

        response = self._call_llm(prompt, model=self.chat_model)
        self._add_to_history('assistant', response, 'hint', {'hint_number': self.hint_count})
        
        return response
    
    def debug_conversation(self, candidate_message: str, failing_code: str, test_results: List[Dict]) -> str:
        """
        Multi-turn debugging conversation using Socratic method
        
        Args:
            candidate_message: What they're saying about the bug
            failing_code: Their current code
            test_results: Which tests are failing
            
        Returns:
            Guiding question or hint
        """
        self.candidate_code = failing_code
        self._add_to_history('user', candidate_message, 'debugging')
        
        # Analyze which tests are failing
        failed_tests = [t for t in test_results if t['status'] != 'passed']
        passed_tests = [t for t in test_results if t['status'] == 'passed']
        
        prompt = f"""You are a debugging mentor using the Socratic method.

**Problem:** {self.problem_data['title']}

**Candidate's code:**
```
{failing_code}
```

**Test Results:**
- Passed: {len(passed_tests)} tests
- Failed: {len(failed_tests)} tests

**Failed test examples:**
{self._format_failed_tests(failed_tests[:2])}

**Candidate says:**
"{candidate_message}"

**Your task:**
Guide them to find the bug themselves using questions:
1. What do they think is causing the failure?
2. Guide them to check specific parts of their code
3. Ask about edge cases
4. Help them trace through logic with a failing example

DO NOT:
- Give away the solution
- Write code for them
- Point directly to the bug

DO:
- Ask probing questions
- Suggest debugging techniques
- Guide their thinking process
- Be encouraging and patient

Keep response under 4 sentences."""

        response = self._call_llm(prompt, model=self.chat_model)
        self._add_to_history('assistant', response, 'debugging')
        
        return response
    
    def analyze_code_submission(self, code: str, test_results: List[Dict]) -> Dict:
        """
        Deep analysis of submitted code using powerful model
        
        Args:
            code: Final submitted code
            test_results: Test case results
            
        Returns:
            Comprehensive analysis with scores
        """
        self.current_stage = self.STAGES['REVIEW']
        self.candidate_code = code
        
        passed_count = sum(1 for t in test_results if t['status'] == 'passed')
        total_count = len(test_results)
        
        prompt = f"""You are an expert code reviewer for a technical interview.

**Problem:** {self.problem_data['title']}

**Candidate's solution:**
```
{code}
```

**Test Results:** {passed_count}/{total_count} passed

**Previous approach discussion:**
{self._get_approach_discussion()}

Provide comprehensive analysis in JSON:
{{
  "code_quality_score": <0-100>,
  "correctness": <0-100>,
  "efficiency": <0-100>,
  "readability": <0-100>,
  "time_complexity": "O(...)",
  "space_complexity": "O(...)",
  "strengths": ["strength1", "strength2", "strength3"],
  "weaknesses": ["weakness1", "weakness2"],
  "optimization_suggestions": ["suggestion1", "suggestion2"],
  "follow_up_questions": [
    "Question about optimization",
    "Question about edge cases",
    "Question about alternative approaches"
  ],
  "overall_feedback": "Detailed conversational feedback"
}}

Be thorough but fair. Consider test results and their approach discussion."""

        response = self._call_llm(prompt, model=self.analysis_model, json_mode=True)
        
        try:
            analysis = json.loads(response)
            self._add_to_history('assistant', analysis['overall_feedback'], 'review')
            return analysis
        except:
            return {
                'code_quality_score': 70,
                'overall_feedback': response
            }
    
    def ask_follow_up_question(self, topic: str = "optimization") -> str:
        """
        Generate intelligent follow-up questions post-submission
        
        Args:
            topic: What to focus on (optimization, edge_cases, alternatives)
            
        Returns:
            Thought-provoking question
        """
        prompt = f"""You are interviewing a candidate who just solved: {self.problem_data['title']}

**Their solution:**
```
{self.candidate_code[:500]}...
```

**Conversation so far:**
{self._get_recent_conversation(3)}

Generate a follow-up question about {topic}:
- If optimization: Ask how to improve time/space complexity
- If edge_cases: Ask about unusual inputs
- If alternatives: Ask about different approaches

Make it specific to their code. Keep it concise (2-3 sentences)."""

        response = self._call_llm(prompt, model=self.chat_model)
        self._add_to_history('assistant', response, 'follow_up')
        
        return response
    
    def evaluate_explanation(self, candidate_answer: str) -> Dict:
        """
        Score candidate's explanation to follow-up questions
        
        Args:
            candidate_answer: Their explanation
            
        Returns:
            Score and feedback
        """
        self._add_to_history('user', candidate_answer, 'follow_up')
        
        prompt = f"""Evaluate this technical explanation:

**Question context:** Last question in conversation
**Candidate's answer:** "{candidate_answer}"

Rate their explanation (JSON format):
{{
  "accuracy": <0-100>,
  "clarity": <0-100>,
  "depth": <0-100>,
  "overall_score": <0-100>,
  "feedback": "Brief encouraging feedback"
}}

Be fair but rigorous."""

        response = self._call_llm(prompt, model=self.analysis_model, json_mode=True)
        
        try:
            scores = json.loads(response)
            self.communication_score = scores.get('overall_score', 70)
            self._add_to_history('assistant', scores['feedback'], 'evaluation')
            return scores
        except:
            return {'overall_score': 70, 'feedback': response}
    
    def get_final_report(self) -> Dict:
        """
        Generate comprehensive interview report
        
        Returns:
            Full interview metrics and transcript
        """
        return {
            'interview_id': f"INT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'problem': self.problem_data.get('title', 'Unknown'),
            'stages_completed': self._get_completed_stages(),
            'approach_quality': self.approach_quality,
            'communication_score': self.communication_score,
            'hints_used': self.hint_count,
            'conversation_history': self.conversation_history,
            'total_messages': len(self.conversation_history),
            'duration_estimate': len(self.conversation_history) * 2,  # ~2 min per exchange
        }
    
    # ==================== Helper Methods ====================
    
    def _call_llm(self, prompt: str, model: str, json_mode: bool = False) -> str:
        """Call Groq LLM with error handling"""
        try:
            messages = [{"role": "user", "content": prompt}]
            
            params = {
                "model": model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1024
            }
            
            if json_mode:
                params["response_format"] = {"type": "json_object"}
            
            response = self.groq_client.chat.completions.create(**params)
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I apologize, I'm having trouble processing that. Could you rephrase? (Error: {str(e)[:50]})"
    
    def _add_to_history(self, role: str, content: str, stage: str, metadata: Dict = None):
        """Add message to conversation history"""
        self.conversation_history.append({
            'role': role,
            'content': content,
            'stage': stage,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        })
    
    def _get_problem_context(self) -> str:
        """Format problem info for prompts"""
        return f"""
Title: {self.problem_data.get('title', 'N/A')}
Difficulty: {self.problem_data.get('difficulty', 'N/A')}
Description: {self.problem_data.get('description', 'N/A')[:200]}...
"""
    
    def _get_recent_conversation(self, n: int = 5) -> str:
        """Get last N conversation exchanges"""
        recent = self.conversation_history[-n:]
        formatted = []
        for msg in recent:
            role = "AI" if msg['role'] == 'assistant' else "Candidate"
            formatted.append(f"{role}: {msg['content'][:100]}...")
        return "\n".join(formatted)
    
    def _get_approach_discussion(self) -> str:
        """Extract approach discussion from history"""
        approach_msgs = [m for m in self.conversation_history if m['stage'] == 'approach']
        return "\n".join([f"{m['role']}: {m['content']}" for m in approach_msgs[-3:]])
    
    def _format_examples(self, examples: List[Dict]) -> str:
        """Format problem examples"""
        formatted = []
        for i, ex in enumerate(examples[:2], 1):
            formatted.append(f"Example {i}:")
            formatted.append(f"  Input: {ex.get('input', 'N/A')}")
            formatted.append(f"  Output: {ex.get('output', 'N/A')}")
            if ex.get('explanation'):
                formatted.append(f"  Explanation: {ex['explanation']}")
        return "\n".join(formatted)
    
    def _format_failed_tests(self, failed_tests: List[Dict]) -> str:
        """Format failed test info"""
        formatted = []
        for test in failed_tests:
            formatted.append(f"- Input: {test.get('input', 'N/A')}")
            formatted.append(f"  Expected: {test.get('expected', 'N/A')}")
            formatted.append(f"  Got: {test.get('output', 'N/A')}")
        return "\n".join(formatted) if formatted else "No failed tests to show"
    
    def _get_completed_stages(self) -> List[str]:
        """Get list of completed interview stages"""
        stages = set()
        for msg in self.conversation_history:
            stages.add(msg['stage'])
        return list(stages)
    
    def get_conversation_for_display(self) -> List[Dict]:
        """Get formatted conversation for UI"""
        return [
            {
                'role': msg['role'],
                'content': msg['content'],
                'stage': msg['stage'],
                'timestamp': msg['timestamp']
            }
            for msg in self.conversation_history
        ]
