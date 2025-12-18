"""
Code Execution Service - Judge0 API Integration with Local Fallback
Executes code in multiple languages with test cases
"""
import requests
import time
from typing import Dict, List, Optional
import base64
import os
from dotenv import load_dotenv
from local_executor import LocalPythonExecutor

load_dotenv()


class CodeExecutor:
    """
    Handles code execution using Judge0 API
    Supports multiple languages and test case validation
    """
    
    # Judge0 API endpoints (using free public instance - no API key needed!)
    BASE_URL = "https://judge0-ce.p.rapidapi.com"
    SULU_URL = "https://ce.judge0.com"  # Free public instance (primary)
    BACKUP_URL = "https://judge0.p.rapidapi.com"  # Backup
    EXTRA_URL = "https://judge0-extra.p.rapidapi.com"  # Extra
    
    # Language IDs for Judge0
    LANGUAGES = {
        'python': 71,      # Python 3.8.1
        'java': 62,        # Java (OpenJDK 13.0.1)
        'cpp': 54,         # C++ (GCC 9.2.0)
        'c': 50,           # C (GCC 9.2.0)
        'javascript': 63,  # JavaScript (Node.js 12.14.0)
    }
    
    def __init__(self):
        self.api_key = os.getenv('JUDGE0_API_KEY', '')
        self.local_executor = LocalPythonExecutor()  # Fallback for Python
        self.use_local = False  # Will switch to True if Judge0 fails
        
        # Use free public instance if no API key
        if not self.api_key:
            self.base_url = self.SULU_URL
            self.headers = {
                "content-type": "application/json"
            }
        else:
            self.base_url = self.BASE_URL
            self.headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": self.api_key,
                "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com"
            }
    
    def execute_code(
        self, 
        code: str, 
        language: str, 
        stdin: str = "", 
        time_limit: float = 2.0,
        memory_limit: int = 128000
    ) -> Dict:
        """
        Execute code with given input
        
        Args:
            code: Source code to execute
            language: Programming language (python, java, cpp, c, javascript)
            stdin: Standard input for the program
            time_limit: CPU time limit in seconds
            memory_limit: Memory limit in KB
            
        Returns:
            Dict with status, output, time, memory, error
        """
        # Use local executor for Python if Judge0 is unavailable
        if self.use_local and language.lower() == 'python':
            return self.local_executor.execute_python(code, stdin, time_limit)
        
        try:
            language_id = self.LANGUAGES.get(language.lower())
            if not language_id:
                return {
                    'status': 'error',
                    'error': f'Unsupported language: {language}',
                    'output': ''
                }
            
            # Encode code and stdin to base64
            code_b64 = base64.b64encode(code.encode()).decode()
            stdin_b64 = base64.b64encode(stdin.encode()).decode() if stdin else ""
            
            # Create submission
            submission_data = {
                "language_id": language_id,
                "source_code": code_b64,
                "stdin": stdin_b64,
                "cpu_time_limit": time_limit,
                "memory_limit": memory_limit
            }
            
            # Submit code
            response = requests.post(
                f"{self.base_url}/submissions?base64_encoded=true&wait=false",
                json=submission_data,
                headers=self.headers,
                timeout=10  # Add timeout to catch slow responses
            )
            
            if response.status_code == 504:
                # Gateway timeout - switch to local executor for Python
                if language.lower() == 'python':
                    self.use_local = True
                    return self.local_executor.execute_python(code, stdin, time_limit)
                else:
                    return {
                        'status': 'error',
                        'error': 'Code execution service is temporarily unavailable. Only Python is supported locally.',
                        'output': ''
                    }
            
            if response.status_code != 201:
                # Try local fallback for Python
                if language.lower() == 'python':
                    self.use_local = True
                    return self.local_executor.execute_python(code, stdin, time_limit)
                
                return {
                    'status': 'error',
                    'error': f'Submission failed: {response.text}',
                    'output': ''
                }
            
            token = response.json()['token']
            
            # Poll for result
            result = self._get_submission_result(token)
            return result
            
        except requests.exceptions.Timeout:
            # Timeout - use local executor for Python
            if language.lower() == 'python':
                self.use_local = True
                return self.local_executor.execute_python(code, stdin, time_limit)
            return {
                'status': 'error',
                'error': 'Request timeout. Code execution service unavailable.',
                'output': '',
                'time': 0,
                'memory': 0
            }
        except Exception as e:
            # Any other error - try local for Python
            if language.lower() == 'python':
                self.use_local = True
                return self.local_executor.execute_python(code, stdin, time_limit)
            return {
                'status': 'error',
                'error': str(e),
                'output': '',
                'time': 0,
                'memory': 0
            }
    
    def _get_submission_result(self, token: str, max_attempts: int = 10) -> Dict:
        """Poll Judge0 for submission result"""
        for _ in range(max_attempts):
            try:
                response = requests.get(
                    f"{self.base_url}/submissions/{token}?base64_encoded=true",
                    headers=self.headers
                )
                
                if response.status_code != 200:
                    time.sleep(1)
                    continue
                
                result = response.json()
                status_id = result.get('status', {}).get('id')
                
                # Status: 1=In Queue, 2=Processing
                if status_id in [1, 2]:
                    time.sleep(1)
                    continue
                
                # Decode output
                stdout = base64.b64decode(result.get('stdout', '') or '').decode('utf-8', errors='ignore')
                stderr = base64.b64decode(result.get('stderr', '') or '').decode('utf-8', errors='ignore')
                compile_output = base64.b64decode(result.get('compile_output', '') or '').decode('utf-8', errors='ignore')
                
                # Status: 3=Accepted
                if status_id == 3:
                    return {
                        'status': 'success',
                        'output': stdout.strip(),
                        'error': '',
                        'time': float(result.get('time', 0) or 0),
                        'memory': int(result.get('memory', 0) or 0)
                    }
                
                # Other statuses (error, TLE, etc.)
                error_msg = stderr or compile_output or result.get('status', {}).get('description', 'Unknown error')
                return {
                    'status': 'error',
                    'output': stdout.strip(),
                    'error': error_msg,
                    'time': float(result.get('time', 0) or 0),
                    'memory': int(result.get('memory', 0) or 0)
                }
                
            except Exception as e:
                time.sleep(1)
                continue
        
        return {
            'status': 'error',
            'error': 'Execution timeout - could not get result',
            'output': '',
            'time': 0,
            'memory': 0
        }
    
    def run_test_cases(
        self, 
        code: str, 
        language: str, 
        test_cases: List[Dict],
        time_limit: float = 2.0
    ) -> Dict:
        """
        Run code against multiple test cases
        
        Args:
            code: Source code
            language: Programming language
            test_cases: List of {'input': str, 'expected': str, 'visible': bool}
            time_limit: Time limit per test case
            
        Returns:
            Dict with overall results and per-test-case details
        """
        results = {
            'total': len(test_cases),
            'passed': 0,
            'failed': 0,
            'error': 0,
            'test_results': [],
            'all_passed': False
        }
        
        for i, test_case in enumerate(test_cases):
            result = self.execute_code(
                code=code,
                language=language,
                stdin=test_case.get('input', ''),
                time_limit=time_limit
            )
            
            # Check if output matches expected
            actual_output = result['output'].strip()
            expected_output = test_case.get('expected', '').strip()
            
            # Debug: Print comparison details (for troubleshooting)
            # print(f"Test {i+1}: Expected '{expected_output}' vs Actual '{actual_output}'")
            
            # Flexible comparison - normalize outputs
            passed = self._compare_outputs(actual_output, expected_output)
            
            if result['status'] == 'success' and passed:
                results['passed'] += 1
                status = 'passed'
            elif result['status'] == 'success' and not passed:
                results['failed'] += 1
                status = 'failed'
            else:
                results['error'] += 1
                status = 'error'
            
            # Only show details for visible test cases
            if test_case.get('visible', True):
                results['test_results'].append({
                    'test_number': i + 1,
                    'status': status,
                    'input': test_case.get('input', ''),
                    'expected': expected_output,
                    'actual': actual_output,
                    'error': result.get('error', ''),
                    'time': result.get('time', 0),
                    'memory': result.get('memory', 0)
                })
            else:
                # Hidden test case - only show pass/fail
                results['test_results'].append({
                    'test_number': i + 1,
                    'status': status,
                    'input': 'Hidden',
                    'expected': 'Hidden',
                    'actual': 'Hidden' if status != 'passed' else expected_output,
                    'error': result.get('error', '') if status == 'error' else '',
                    'time': result.get('time', 0),
                    'memory': result.get('memory', 0),
                    'hidden': True
                })
        
        results['all_passed'] = (results['passed'] == results['total'])
        return results
    
    def _compare_outputs(self, actual: str, expected: str) -> bool:
        """Flexible output comparison that handles common format variations"""
        # Direct match
        if actual == expected:
            return True
        
        # Normalize: remove brackets, commas, extra whitespace
        def normalize(s):
            # Remove common formatting characters
            s = s.replace('[', '').replace(']', '').replace('(', '').replace(')', '')
            s = s.replace(',', ' ').replace('\t', ' ')
            # Split and rejoin to normalize whitespace
            tokens = s.split()
            return ' '.join(tokens)
        
        actual_norm = normalize(actual)
        expected_norm = normalize(expected)
        
        # Compare normalized versions (order matters!)
        return actual_norm == expected_norm


# Test function
def test_executor():
    """Quick test of code executor"""
    executor = CodeExecutor()
    
    # Test Python
    python_code = """
n = int(input())
print(n * 2)
"""
    
    result = executor.execute_code(python_code, 'python', '5')
    print("Python test:", result)
    
    # Test with test cases
    test_cases = [
        {'input': '5', 'expected': '10', 'visible': True},
        {'input': '100', 'expected': '200', 'visible': False}
    ]
    
    results = executor.run_test_cases(python_code, 'python', test_cases)
    print("Test cases:", results)


if __name__ == "__main__":
    test_executor()
