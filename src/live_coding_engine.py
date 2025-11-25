"""
💻 LIVE CODING CHALLENGE ENGINE
Safe code execution environment for programming skill verification
"""

import subprocess
import tempfile
import os
import json
import time
import hashlib
import re
import signal
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import threading
import queue

class SecureCodeExecutor:
    """
    Secure environment for executing user code with safety restrictions
    """
    
    def __init__(self):
        self.execution_timeout = 10  # seconds
        self.memory_limit = 128  # MB (would need platform-specific implementation)
        self.allowed_imports = {
            'python': [
                'math', 'random', 'datetime', 'collections', 'itertools',
                'functools', 'operator', 'heapq', 're', 'string', 'bisect'
            ],
            'java': ['java.util.*', 'java.lang.*', 'java.math.*'],
            'javascript': ['Math', 'Date', 'Array', 'Object', 'String']
        }
        
        # Blacklisted functions/modules for security
        self.security_blacklist = [
            'import os', 'import sys', 'import subprocess', 'import socket',
            'open(', 'file(', 'input(', 'raw_input(', 'eval(', 'exec(',
            '__import__', 'compile(', 'globals()', 'locals()',
            'getattr', 'setattr', 'delattr', 'hasattr'
        ]
        
    def execute_python_code(self, code: str, test_cases: List[Dict], function_name: str) -> Dict[str, Any]:
        """
        Execute Python code with comprehensive testing and security
        """
        # Security check
        security_result = self._check_code_security(code)
        if not security_result['safe']:
            return {
                'success': False,
                'error': 'Security violation: ' + security_result['reason'],
                'test_results': [],
                'execution_time': 0
            }
        
        # Prepare test execution environment
        test_results = []
        start_time = time.time()
        
        try:
            # Create isolated execution environment
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                # Build complete test script
                test_script = self._build_python_test_script(code, test_cases, function_name)
                f.write(test_script)
                temp_file = f.name
            
            # Execute with timeout and capture results
            process = subprocess.Popen(
                ['python', temp_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=os.setsid if os.name != 'nt' else None
            )
            
            try:
                stdout, stderr = process.communicate(timeout=self.execution_timeout)
                execution_time = time.time() - start_time
                
                # Parse results
                if process.returncode == 0 and stdout:
                    test_results = self._parse_python_results(stdout)
                    
                    return {
                        'success': True,
                        'test_results': test_results,
                        'execution_time': execution_time,
                        'all_passed': all(result['passed'] for result in test_results),
                        'score': self._calculate_score(test_results),
                        'performance_metrics': self._analyze_performance(code, execution_time)
                    }
                else:
                    return {
                        'success': False,
                        'error': stderr or 'Code execution failed',
                        'test_results': [],
                        'execution_time': execution_time
                    }
                    
            except subprocess.TimeoutExpired:
                # Kill the process tree
                if os.name != 'nt':
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                else:
                    process.terminate()
                    
                return {
                    'success': False,
                    'error': f'Code execution timed out after {self.execution_timeout} seconds',
                    'test_results': [],
                    'execution_time': self.execution_timeout
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Execution error: {str(e)}',
                'test_results': [],
                'execution_time': time.time() - start_time
            }
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file)
            except:
                pass
    
    def execute_java_code(self, code: str, test_cases: List[Dict], class_name: str) -> Dict[str, Any]:
        """
        Execute Java code with testing
        """
        start_time = time.time()
        
        try:
            # Create temporary directory for Java compilation
            with tempfile.TemporaryDirectory() as temp_dir:
                java_file = os.path.join(temp_dir, f"{class_name}.java")
                
                # Write Java code to file
                with open(java_file, 'w') as f:
                    f.write(code)
                
                # Compile Java code
                compile_process = subprocess.run(
                    ['javac', java_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if compile_process.returncode != 0:
                    return {
                        'success': False,
                        'error': f'Compilation error: {compile_process.stderr}',
                        'test_results': [],
                        'execution_time': time.time() - start_time
                    }
                
                # Execute compiled Java class
                # This would require a more complex setup with test harness
                return {
                    'success': True,
                    'test_results': [],  # Placeholder
                    'execution_time': time.time() - start_time,
                    'message': 'Java execution not fully implemented in this demo'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Java execution error: {str(e)}',
                'test_results': [],
                'execution_time': time.time() - start_time
            }
    
    def _check_code_security(self, code: str) -> Dict[str, Any]:
        """
        Check code for security violations
        """
        code_lower = code.lower()
        
        for blacklisted in self.security_blacklist:
            if blacklisted.lower() in code_lower:
                return {
                    'safe': False,
                    'reason': f'Prohibited operation detected: {blacklisted}'
                }
        
        # Check for excessive recursion patterns
        if code.count('def ') > 10:
            return {
                'safe': False,
                'reason': 'Too many function definitions'
            }
        
        # Check for infinite loop patterns
        suspicious_patterns = ['while True:', 'while 1:', 'for i in range(99999']
        for pattern in suspicious_patterns:
            if pattern in code:
                return {
                    'safe': False,
                    'reason': f'Potentially infinite loop detected: {pattern}'
                }
        
        return {'safe': True, 'reason': 'Code passed security checks'}
    
    def _build_python_test_script(self, user_code: str, test_cases: List[Dict], function_name: str) -> str:
        """
        Build complete Python test script with user code and test cases
        """
        test_script = f"""
import json
import sys
import traceback

# User's code
{user_code}

# Test execution
test_results = []

test_cases = {json.dumps(test_cases)}

for i, test_case in enumerate(test_cases):
    try:
        # Get input parameters
        if isinstance(test_case['input'], list) and len(test_case['input']) == 1:
            # Single parameter
            result = {function_name}(test_case['input'][0])
        elif isinstance(test_case['input'], list):
            # Multiple parameters
            result = {function_name}(*test_case['input'])
        else:
            # Single non-list parameter
            result = {function_name}(test_case['input'])
        
        expected = test_case['expected']
        passed = result == expected
        
        test_results.append({{
            'test_case': i + 1,
            'input': test_case['input'],
            'expected': expected,
            'actual': result,
            'passed': passed,
            'error': None
        }})
        
    except Exception as e:
        test_results.append({{
            'test_case': i + 1,
            'input': test_case['input'],
            'expected': test_case['expected'],
            'actual': None,
            'passed': False,
            'error': str(e)
        }})

# Output results as JSON
print("RESULTS_START")
print(json.dumps(test_results))
print("RESULTS_END")
"""
        return test_script
    
    def _parse_python_results(self, stdout: str) -> List[Dict]:
        """
        Parse Python execution results from stdout
        """
        try:
            # Extract JSON results between markers
            start_marker = "RESULTS_START"
            end_marker = "RESULTS_END"
            
            start_idx = stdout.find(start_marker)
            end_idx = stdout.find(end_marker)
            
            if start_idx == -1 or end_idx == -1:
                return []
            
            json_str = stdout[start_idx + len(start_marker):end_idx].strip()
            return json.loads(json_str)
            
        except Exception as e:
            return [{
                'test_case': 1,
                'input': 'unknown',
                'expected': 'unknown',
                'actual': None,
                'passed': False,
                'error': f'Result parsing error: {str(e)}'
            }]
    
    def _calculate_score(self, test_results: List[Dict]) -> float:
        """
        Calculate overall score based on test results
        """
        if not test_results:
            return 0.0
        
        passed_tests = sum(1 for result in test_results if result['passed'])
        return (passed_tests / len(test_results)) * 100
    
    def _analyze_performance(self, code: str, execution_time: float) -> Dict[str, Any]:
        """
        Analyze code performance and quality
        """
        metrics = {
            'execution_time': execution_time,
            'code_length': len(code),
            'time_complexity_estimate': 'O(n)',  # Placeholder
            'space_complexity_estimate': 'O(1)',  # Placeholder
            'quality_indicators': []
        }
        
        # Basic quality analysis
        if 'for ' in code or 'while ' in code:
            metrics['quality_indicators'].append('Uses loops effectively')
        
        if 'def ' in code:
            metrics['quality_indicators'].append('Well-structured with functions')
        
        if execution_time < 0.1:
            metrics['quality_indicators'].append('Efficient execution time')
        
        if len(code.split('\n')) < 20:
            metrics['quality_indicators'].append('Concise implementation')
        
        return metrics

class LiveCodingChallengeManager:
    """
    Manages live coding challenges and user sessions
    """
    
    def __init__(self):
        self.executor = SecureCodeExecutor()
        self.challenge_database = self._load_challenge_database()
        self.active_sessions = {}  # session_id -> session_data
    
    def start_coding_session(self, user_id: int, skill: str, difficulty: str = 'medium') -> Dict[str, Any]:
        """
        Start a new live coding session
        """
        # Generate session ID
        session_id = hashlib.md5(f"{user_id}_{skill}_{time.time()}".encode()).hexdigest()[:16]
        
        # Get challenge for skill and difficulty
        challenge = self._get_challenge(skill, difficulty)
        
        if not challenge:
            return {
                'success': False,
                'error': f'No challenge available for {skill} at {difficulty} level'
            }
        
        # Create session
        session_data = {
            'session_id': session_id,
            'user_id': user_id,
            'skill': skill,
            'difficulty': difficulty,
            'challenge': challenge,
            'start_time': datetime.now(),
            'time_limit': challenge.get('time_limit', 15) * 60,  # Convert to seconds
            'attempts': 0,
            'max_attempts': 3,
            'status': 'active'
        }
        
        self.active_sessions[session_id] = session_data
        
        return {
            'success': True,
            'session_id': session_id,
            'challenge': {
                'title': challenge['title'],
                'description': challenge['description'],
                'function_signature': challenge.get('function_signature', ''),
                'starter_code': challenge.get('starter_code', ''),
                'language': challenge.get('language', skill),
                'time_limit': challenge.get('time_limit', 15),
                'example_input': challenge.get('example_input'),
                'example_output': challenge.get('example_output')
            },
            'session_info': {
                'time_limit': session_data['time_limit'],
                'attempts_remaining': session_data['max_attempts']
            }
        }
    
    def submit_code(self, session_id: str, code: str) -> Dict[str, Any]:
        """
        Submit code for evaluation
        """
        session = self.active_sessions.get(session_id)
        if not session:
            return {
                'success': False,
                'error': 'Invalid session ID'
            }
        
        # Check if session is still active
        elapsed_time = (datetime.now() - session['start_time']).total_seconds()
        if elapsed_time > session['time_limit']:
            session['status'] = 'expired'
            return {
                'success': False,
                'error': 'Session has expired'
            }
        
        # Check attempts
        if session['attempts'] >= session['max_attempts']:
            session['status'] = 'max_attempts_reached'
            return {
                'success': False,
                'error': 'Maximum attempts reached'
            }
        
        # Increment attempts
        session['attempts'] += 1
        
        # Execute code
        challenge = session['challenge']
        test_cases = challenge.get('test_cases', [])
        function_name = self._extract_function_name(challenge.get('function_signature', ''))
        
        if session['skill'].lower() == 'python':
            execution_result = self.executor.execute_python_code(code, test_cases, function_name)
        elif session['skill'].lower() == 'java':
            execution_result = self.executor.execute_java_code(code, test_cases, 'Solution')
        else:
            return {
                'success': False,
                'error': f'Language {session["skill"]} not supported yet'
            }
        
        # Evaluate results
        verification_passed = execution_result.get('all_passed', False) and execution_result.get('score', 0) >= 70
        
        # Update session
        session['last_submission'] = {
            'code': code,
            'result': execution_result,
            'timestamp': datetime.now(),
            'verification_passed': verification_passed
        }
        
        if verification_passed:
            session['status'] = 'completed'
        elif session['attempts'] >= session['max_attempts']:
            session['status'] = 'failed'
        
        # Prepare response
        response = {
            'success': execution_result['success'],
            'verification_passed': verification_passed,
            'execution_result': execution_result,
            'session_status': session['status'],
            'attempts_remaining': session['max_attempts'] - session['attempts'],
            'time_remaining': session['time_limit'] - elapsed_time
        }
        
        # Add feedback and hints for failed attempts
        if not verification_passed and session['attempts'] < session['max_attempts']:
            response['hints'] = self._generate_hints(challenge, execution_result)
        
        return response
    
    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """
        Get current session status
        """
        session = self.active_sessions.get(session_id)
        if not session:
            return {
                'success': False,
                'error': 'Session not found'
            }
        
        elapsed_time = (datetime.now() - session['start_time']).total_seconds()
        
        return {
            'success': True,
            'session_id': session_id,
            'status': session['status'],
            'skill': session['skill'],
            'difficulty': session['difficulty'],
            'attempts_used': session['attempts'],
            'attempts_remaining': session['max_attempts'] - session['attempts'],
            'time_elapsed': elapsed_time,
            'time_remaining': max(0, session['time_limit'] - elapsed_time),
            'challenge_title': session['challenge']['title']
        }
    
    def _get_challenge(self, skill: str, difficulty: str) -> Optional[Dict[str, Any]]:
        """
        Get challenge from database
        """
        skill_challenges = self.challenge_database.get(skill.lower(), {})
        return skill_challenges.get(difficulty, None)
    
    def _extract_function_name(self, function_signature: str) -> str:
        """
        Extract function name from signature
        """
        # For Python: "def function_name(params):" -> "function_name"
        match = re.search(r'def\s+(\w+)\s*\(', function_signature)
        if match:
            return match.group(1)
        
        # Default fallback
        return 'solution'
    
    def _generate_hints(self, challenge: Dict, execution_result: Dict) -> List[str]:
        """
        Generate helpful hints based on execution results
        """
        hints = []
        
        if not execution_result.get('success', False):
            hints.append("💡 Check for syntax errors or runtime exceptions")
        
        test_results = execution_result.get('test_results', [])
        failed_tests = [t for t in test_results if not t.get('passed', False)]
        
        if failed_tests:
            if len(failed_tests) == len(test_results):
                hints.append("🔍 Your function might not be returning the expected value")
            else:
                hints.append(f"⚠️ {len(failed_tests)} out of {len(test_results)} test cases failed")
            
            # Analyze common failure patterns
            error_types = [t.get('error', '') for t in failed_tests if t.get('error')]
            if any('IndexError' in error for error in error_types):
                hints.append("🚨 Check array bounds - you might be accessing invalid indices")
            if any('TypeError' in error for error in error_types):
                hints.append("🔧 Check data types - ensure you're using the right type operations")
        
        return hints
    
    def _load_challenge_database(self) -> Dict[str, Dict[str, Dict]]:
        """
        Load coding challenges database
        """
        return {
            'python': {
                'easy': {
                    'title': 'Find Second Largest',
                    'description': 'Write a function that finds the second largest number in a list.',
                    'function_signature': 'def find_second_largest(numbers):',
                    'starter_code': 'def find_second_largest(numbers):\n    # Your code here\n    pass',
                    'test_cases': [
                        {'input': [[1, 3, 4, 5, 2]], 'expected': 4},
                        {'input': [[10, 20, 30]], 'expected': 20},
                        {'input': [[1, 1, 2, 2]], 'expected': 1},
                        {'input': [[5]], 'expected': None}
                    ],
                    'time_limit': 10,
                    'example_input': '[1, 3, 4, 5, 2]',
                    'example_output': '4'
                },
                'medium': {
                    'title': 'Valid Parentheses',
                    'description': 'Determine if a string of parentheses is valid.',
                    'function_signature': 'def is_valid_parentheses(s):',
                    'starter_code': 'def is_valid_parentheses(s):\n    # Your code here\n    pass',
                    'test_cases': [
                        {'input': ['()'], 'expected': True},
                        {'input': ['()[]{}'], 'expected': True},
                        {'input': ['(]'], 'expected': False},
                        {'input': ['([)]'], 'expected': False},
                        {'input': ['{[]}'], 'expected': True}
                    ],
                    'time_limit': 15,
                    'example_input': '"()[]"',
                    'example_output': 'True'
                },
                'hard': {
                    'title': 'Longest Common Subsequence',
                    'description': 'Find the length of the longest common subsequence.',
                    'function_signature': 'def longest_common_subsequence(text1, text2):',
                    'starter_code': 'def longest_common_subsequence(text1, text2):\n    # Your code here\n    pass',
                    'test_cases': [
                        {'input': ['abcde', 'ace'], 'expected': 3},
                        {'input': ['abc', 'abc'], 'expected': 3},
                        {'input': ['abc', 'def'], 'expected': 0}
                    ],
                    'time_limit': 20
                }
            },
            'java': {
                'easy': {
                    'title': 'Palindrome Check',
                    'description': 'Check if a string is a palindrome.',
                    'function_signature': 'public static boolean isPalindrome(String str)',
                    'time_limit': 12
                }
            }
        }

# Example usage
if __name__ == "__main__":
    # Test the live coding system
    manager = LiveCodingChallengeManager()
    
    # Start a session
    session = manager.start_coding_session(user_id=1, skill='python', difficulty='easy')
    print("🚀 Session Started:")
    print(f"Session ID: {session['session_id']}")
    print(f"Challenge: {session['challenge']['title']}")
    print(f"Description: {session['challenge']['description']}")
    
    # Test code submission
    test_code = """
def find_second_largest(numbers):
    if len(numbers) < 2:
        return None
    
    unique_numbers = list(set(numbers))
    if len(unique_numbers) < 2:
        return None
    
    unique_numbers.sort(reverse=True)
    return unique_numbers[1]
"""
    
    result = manager.submit_code(session['session_id'], test_code)
    print(f"\n✅ Code Execution Result:")
    print(f"Success: {result['success']}")
    print(f"Verification Passed: {result['verification_passed']}")
    if result['execution_result']:
        print(f"Score: {result['execution_result']['score']:.1f}%")
        print(f"All Tests Passed: {result['execution_result']['all_passed']}")
    
    print("\n🎯 Live Coding Engine ready for integration!")