"""
Local Python Code Executor - Fallback for when Judge0 is unavailable
Runs Python code safely in subprocess with timeout
"""
import subprocess
import time
from typing import Dict


class LocalPythonExecutor:
    """
    Execute Python code locally in a safe subprocess
    Works as fallback when Judge0 API is unavailable
    """
    
    def execute_python(self, code: str, stdin: str = "", timeout: float = 5.0) -> Dict:
        """
        Execute Python code locally
        
        Args:
            code: Python source code
            stdin: Input to pass to the program
            timeout: Maximum execution time in seconds
            
        Returns:
            Dict with status, output, error, time
        """
        try:
            start_time = time.time()
            
            # Run Python code in subprocess
            process = subprocess.Popen(
                ['python', '-c', code],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Communicate with timeout
            try:
                stdout, stderr = process.communicate(input=stdin, timeout=timeout)
                execution_time = time.time() - start_time
                
                if process.returncode == 0:
                    return {
                        'status': 'success',
                        'output': stdout.strip(),
                        'error': '',
                        'time': execution_time,
                        'memory': 0  # Not tracked locally
                    }
                else:
                    return {
                        'status': 'error',
                        'output': stdout.strip(),
                        'error': stderr.strip(),
                        'time': execution_time,
                        'memory': 0
                    }
                    
            except subprocess.TimeoutExpired:
                process.kill()
                return {
                    'status': 'error',
                    'output': '',
                    'error': f'Time Limit Exceeded ({timeout}s)',
                    'time': timeout,
                    'memory': 0
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'output': '',
                'error': f'Execution failed: {str(e)}',
                'time': 0,
                'memory': 0
            }
