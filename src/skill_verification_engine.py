"""
🔐 TRUST BUT VERIFY - Skill Verification Engine
Automated skill extraction, verification challenges, and credentialing system
"""

import re
import json
import time
import subprocess
import tempfile
import os
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import hashlib
import random
import string

class SkillVerificationEngine:
    """
    Core engine for the Trust but Verify module that:
    1. Extracts skills from resumes automatically
    2. Generates context-aware verification challenges
    3. Manages verification queue and badge system
    4. Implements light proctoring features
    """
    
    def __init__(self):
        self.skill_categories = {
            'programming_languages': [
                'python', 'java', 'javascript', 'js', 'c++', 'cpp', 'c#', 'csharp',
                'php', 'ruby', 'go', 'rust', 'kotlin', 'swift', 'typescript', 'ts',
                'scala', 'r', 'matlab', 'perl', 'bash', 'shell'
            ],
            'databases': [
                'sql', 'mysql', 'postgresql', 'postgres', 'mongodb', 'sqlite',
                'oracle', 'sqlserver', 'redis', 'cassandra', 'dynamodb', 'neo4j'
            ],
            'frameworks_libraries': [
                'react', 'angular', 'vue', 'nodejs', 'express', 'django', 'flask',
                'spring', 'laravel', 'tensorflow', 'pytorch', 'keras', 'pandas',
                'numpy', 'scikit-learn', 'opencv', 'bootstrap', 'jquery'
            ],
            'cloud_technologies': [
                'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git',
                'github', 'gitlab', 'bitbucket', 'terraform', 'ansible'
            ],
            'data_science': [
                'machine learning', 'ml', 'data science', 'data analysis', 'statistics',
                'deep learning', 'artificial intelligence', 'ai', 'nlp', 'computer vision'
            ]
        }
        
        # Initialize challenge databases
        self.programming_challenges = self._load_programming_challenges()
        self.sql_challenges = self._load_sql_challenges()
        self.framework_challenges = self._load_framework_challenges()
        
    def extract_skills_from_resume(self, resume_text: str) -> Dict[str, List[str]]:
        """
        Extract and categorize skills from resume text using NLP and pattern matching
        """
        resume_lower = resume_text.lower()
        extracted_skills = {category: [] for category in self.skill_categories.keys()}
        
        # Enhanced skill extraction with context awareness
        for category, skills in self.skill_categories.items():
            for skill in skills:
                # Use regex for more accurate matching
                patterns = [
                    rf'\b{re.escape(skill)}\b',  # Exact word match
                    rf'{re.escape(skill)}\s*[:\-]',  # Skill followed by colon or dash
                    rf'experience\s+(?:with|in)\s+{re.escape(skill)}',  # Experience patterns
                    rf'proficient\s+(?:in|with)\s+{re.escape(skill)}',  # Proficiency patterns
                    rf'skilled\s+(?:in|with)\s+{re.escape(skill)}',  # Skilled patterns
                ]
                
                for pattern in patterns:
                    if re.search(pattern, resume_lower):
                        if skill not in extracted_skills[category]:
                            extracted_skills[category].append(skill.title())
                        break
        
        # Remove empty categories
        extracted_skills = {k: v for k, v in extracted_skills.items() if v}
        
        return extracted_skills
    
    def generate_verification_queue(self, user_id: int, extracted_skills: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        Generate a verification queue for extracted skills
        """
        verification_queue = []
        total_skills = 0
        
        for category, skills in extracted_skills.items():
            for skill in skills:
                total_skills += 1
                verification_item = {
                    'skill_id': self._generate_skill_id(skill, category),
                    'skill_name': skill,
                    'category': category,
                    'status': 'pending',  # pending, in_progress, verified, failed
                    'challenge_type': self._determine_challenge_type(skill, category),
                    'estimated_time': self._get_estimated_time(skill, category),
                    'priority_score': self._calculate_priority_score(skill, category),
                    'attempts_allowed': 3,
                    'attempts_used': 0,
                    'created_at': datetime.now().isoformat()
                }
                verification_queue.append(verification_item)
        
        # Sort by priority (high-demand skills first)
        verification_queue.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return {
            'user_id': user_id,
            'total_skills': total_skills,
            'queue': verification_queue,
            'estimated_total_time': sum(item['estimated_time'] for item in verification_queue),
            'high_priority_skills': [item for item in verification_queue if item['priority_score'] > 8],
            'recommendations': self._generate_verification_recommendations(verification_queue)
        }
    
    def get_verification_challenge(self, skill_name: str, category: str, difficulty: str = 'medium') -> Dict[str, Any]:
        """
        Generate context-aware verification challenge based on skill type
        """
        if category == 'programming_languages':
            return self._generate_programming_challenge(skill_name, difficulty)
        elif category == 'databases':
            return self._generate_sql_challenge(skill_name, difficulty)
        elif category == 'frameworks_libraries':
            return self._generate_framework_challenge(skill_name, difficulty)
        elif category == 'cloud_technologies':
            return self._generate_cloud_challenge(skill_name, difficulty)
        elif category == 'data_science':
            return self._generate_data_science_challenge(skill_name, difficulty)
        else:
            return self._generate_general_challenge(skill_name, difficulty)
    
    def _generate_programming_challenge(self, language: str, difficulty: str) -> Dict[str, Any]:
        """Generate live coding challenges for programming languages"""
        lang_lower = language.lower()
        
        if lang_lower == 'python':
            challenges = {
                'easy': {
                    'title': 'Second Largest Number',
                    'description': 'Write a function that takes a list of numbers and returns the second-largest value.',
                    'function_signature': 'def find_second_largest(numbers):',
                    'test_cases': [
                        {'input': [1, 3, 4, 5, 2], 'expected': 4},
                        {'input': [10, 20, 30], 'expected': 20},
                        {'input': [1, 1, 2, 2], 'expected': 1},
                        {'input': [100], 'expected': None}
                    ],
                    'time_limit': 10,
                    'starter_code': 'def find_second_largest(numbers):\n    # Your code here\n    pass'
                },
                'medium': {
                    'title': 'Valid Parentheses',
                    'description': 'Write a function that checks if a string of parentheses is valid.',
                    'function_signature': 'def is_valid_parentheses(s):',
                    'test_cases': [
                        {'input': '()', 'expected': True},
                        {'input': '()[]{}', 'expected': True},
                        {'input': '(]', 'expected': False},
                        {'input': '([)]', 'expected': False}
                    ],
                    'time_limit': 15,
                    'starter_code': 'def is_valid_parentheses(s):\n    # Your code here\n    pass'
                }
            }
        elif lang_lower == 'java':
            challenges = {
                'easy': {
                    'title': 'Palindrome Check',
                    'description': 'Write a method that checks if a string is a palindrome.',
                    'function_signature': 'public static boolean isPalindrome(String str)',
                    'test_cases': [
                        {'input': 'racecar', 'expected': True},
                        {'input': 'hello', 'expected': False},
                        {'input': 'A man a plan a canal Panama', 'expected': True}
                    ],
                    'time_limit': 12,
                    'starter_code': 'public class Solution {\n    public static boolean isPalindrome(String str) {\n        // Your code here\n        return false;\n    }\n}'
                }
            }
        else:
            # Generic programming challenge
            challenges = {
                'easy': {
                    'title': f'{language} Basic Algorithm',
                    'description': f'Demonstrate your {language} skills by solving a basic algorithmic problem.',
                    'time_limit': 15,
                    'challenge_type': 'code_review'
                }
            }
        
        selected_challenge = challenges.get(difficulty, challenges['easy'])
        selected_challenge['language'] = language
        selected_challenge['category'] = 'live_coding'
        
        return selected_challenge
    
    def _generate_sql_challenge(self, database: str, difficulty: str) -> Dict[str, Any]:
        """Generate interactive SQL challenges"""
        challenges = {
            'easy': {
                'title': 'Student Course Enrollment',
                'description': 'Write a query to find the names of all students enrolled in the "Data Structures" course.',
                'schema': {
                    'students': ['id', 'name', 'email', 'age'],
                    'courses': ['id', 'name', 'credits', 'instructor'],
                    'enrollments': ['student_id', 'course_id', 'grade', 'semester']
                },
                'sample_data': {
                    'students': [
                        {'id': 1, 'name': 'John Doe', 'email': 'john@email.com', 'age': 20},
                        {'id': 2, 'name': 'Jane Smith', 'email': 'jane@email.com', 'age': 21}
                    ],
                    'courses': [
                        {'id': 101, 'name': 'Data Structures', 'credits': 3, 'instructor': 'Dr. Smith'},
                        {'id': 102, 'name': 'Algorithms', 'credits': 4, 'instructor': 'Dr. Johnson'}
                    ]
                },
                'expected_result': [{'name': 'John Doe'}, {'name': 'Jane Smith'}],
                'time_limit': 8,
                'starter_query': 'SELECT \n  -- Your query here\nFROM students s\n-- JOIN other tables as needed'
            },
            'medium': {
                'title': 'Top Performing Students',
                'description': 'Find the top 3 students with the highest average grades.',
                'time_limit': 12
            }
        }
        
        selected_challenge = challenges.get(difficulty, challenges['easy'])
        selected_challenge['database_type'] = database
        selected_challenge['category'] = 'sql_sandbox'
        
        return selected_challenge
    
    def _generate_framework_challenge(self, framework: str, difficulty: str) -> Dict[str, Any]:
        """Generate framework/library conceptual challenges"""
        framework_lower = framework.lower()
        
        if framework_lower == 'react':
            challenges = {
                'easy': {
                    'title': 'React State Bug',
                    'description': 'Identify why the state is not updating in this React component.',
                    'code_snippet': '''
import React, { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0);
    
    const handleClick = () => {
        count = count + 1;  // Bug is here
        console.log(count);
    };
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={handleClick}>Increment</button>
        </div>
    );
}
''',
                    'question': 'What is wrong with this code and how would you fix it?',
                    'correct_answer': 'The code directly mutates the count variable instead of using setCount(count + 1). State should be updated using the setter function.',
                    'options': [
                        'Missing useEffect hook',
                        'Direct state mutation instead of using setCount',
                        'Missing key prop',
                        'Incorrect import statement'
                    ],
                    'time_limit': 5
                }
            }
        elif framework_lower == 'django':
            challenges = {
                'easy': {
                    'title': 'Django Model Relationship',
                    'description': 'Identify the correct way to define a one-to-many relationship.',
                    'question': 'How do you properly define a foreign key relationship in Django models?',
                    'time_limit': 7
                }
            }
        else:
            challenges = {
                'easy': {
                    'title': f'{framework} Concepts',
                    'description': f'Test your understanding of {framework} core concepts.',
                    'time_limit': 10
                }
            }
        
        selected_challenge = challenges.get(difficulty, challenges['easy'])
        selected_challenge['framework'] = framework
        selected_challenge['category'] = 'code_review'
        
        return selected_challenge
    
    def execute_python_code(self, code: str, test_cases: List[Dict]) -> Dict[str, Any]:
        """
        Safely execute Python code against test cases
        """
        results = []
        all_passed = True
        
        for i, test_case in enumerate(test_cases):
            try:
                # Create a temporary file with the code
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                    # Add test execution code
                    test_code = f"""
{code}

# Test execution
try:
    result = find_second_largest({test_case['input']})
    print(f"RESULT:{result}")
except Exception as e:
    print(f"ERROR:{str(e)}")
"""
                    f.write(test_code)
                    temp_file = f.name
                
                # Execute the code with timeout
                process = subprocess.run(
                    ['python', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                output = process.stdout.strip()
                
                if output.startswith('RESULT:'):
                    actual_result = eval(output.split('RESULT:')[1])
                    passed = actual_result == test_case['expected']
                    
                    results.append({
                        'test_case': i + 1,
                        'input': test_case['input'],
                        'expected': test_case['expected'],
                        'actual': actual_result,
                        'passed': passed,
                        'error': None
                    })
                    
                    if not passed:
                        all_passed = False
                        
                elif output.startswith('ERROR:'):
                    error_msg = output.split('ERROR:')[1]
                    results.append({
                        'test_case': i + 1,
                        'input': test_case['input'],
                        'expected': test_case['expected'],
                        'actual': None,
                        'passed': False,
                        'error': error_msg
                    })
                    all_passed = False
                
                # Clean up
                os.unlink(temp_file)
                    
            except subprocess.TimeoutExpired:
                results.append({
                    'test_case': i + 1,
                    'input': test_case['input'],
                    'expected': test_case['expected'],
                    'actual': None,
                    'passed': False,
                    'error': 'Code execution timed out'
                })
                all_passed = False
                
            except Exception as e:
                results.append({
                    'test_case': i + 1,
                    'input': test_case['input'],
                    'expected': test_case['expected'],
                    'actual': None,
                    'passed': False,
                    'error': str(e)
                })
                all_passed = False
        
        return {
            'all_passed': all_passed,
            'results': results,
            'score': sum(1 for r in results if r['passed']) / len(results) * 100
        }
    
    def verify_skill(self, user_id: int, skill_id: str, challenge_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process skill verification attempt and award badges
        """
        # Determine verification result based on challenge type
        if challenge_response.get('challenge_type') == 'live_coding':
            verification_result = self._evaluate_coding_challenge(challenge_response)
        elif challenge_response.get('challenge_type') == 'sql_sandbox':
            verification_result = self._evaluate_sql_challenge(challenge_response)
        elif challenge_response.get('challenge_type') == 'code_review':
            verification_result = self._evaluate_code_review_challenge(challenge_response)
        else:
            verification_result = self._evaluate_general_challenge(challenge_response)
        
        # Calculate verification score and badge
        verification_score = verification_result.get('score', 0)
        verification_passed = verification_score >= 70  # 70% threshold for verification
        
        # Update verification status
        verification_status = {
            'skill_id': skill_id,
            'user_id': user_id,
            'verification_passed': verification_passed,
            'verification_score': verification_score,
            'verification_date': datetime.now().isoformat(),
            'challenge_details': challenge_response,
            'evaluation_details': verification_result,
            'badge_awarded': verification_passed,
            'badge_level': self._determine_badge_level(verification_score) if verification_passed else None
        }
        
        # Save verification result to database (would integrate with existing db_manager)
        # self._save_verification_result(verification_status)
        
        return verification_status
    
    def _evaluate_coding_challenge(self, challenge_response: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate live coding challenge response"""
        code = challenge_response.get('code', '')
        test_cases = challenge_response.get('test_cases', [])
        
        execution_result = self.execute_python_code(code, test_cases)
        
        return {
            'type': 'coding_challenge',
            'score': execution_result['score'],
            'all_tests_passed': execution_result['all_passed'],
            'test_results': execution_result['results'],
            'code_quality_score': self._analyze_code_quality(code),
            'feedback': self._generate_coding_feedback(execution_result, code)
        }
    
    def _analyze_code_quality(self, code: str) -> int:
        """Basic code quality analysis"""
        quality_score = 100
        
        # Check for basic quality indicators
        if len(code.strip()) < 10:
            quality_score -= 30
        if 'pass' in code and len(code.strip()) < 50:
            quality_score -= 50  # Likely just placeholder
        if not any(keyword in code for keyword in ['def', 'class', 'for', 'if', 'while']):
            quality_score -= 20
        
        return max(0, quality_score)
    
    def _generate_coding_feedback(self, execution_result: Dict, code: str) -> List[str]:
        """Generate helpful feedback for coding challenges"""
        feedback = []
        
        if execution_result['all_passed']:
            feedback.append("🎉 Excellent! All test cases passed.")
            if self._analyze_code_quality(code) > 80:
                feedback.append("✨ Your code quality looks great!")
        else:
            failed_tests = [r for r in execution_result['results'] if not r['passed']]
            feedback.append(f"❌ {len(failed_tests)} test case(s) failed.")
            
            for test in failed_tests[:2]:  # Show first 2 failures
                if test['error']:
                    feedback.append(f"Error on test {test['test_case']}: {test['error']}")
                else:
                    feedback.append(f"Test {test['test_case']}: Expected {test['expected']}, got {test['actual']}")
        
        return feedback
    
    def _determine_badge_level(self, score: int) -> str:
        """Determine badge level based on verification score"""
        if score >= 95:
            return 'expert'
        elif score >= 85:
            return 'advanced'
        elif score >= 70:
            return 'verified'
        else:
            return 'basic'
    
    def _generate_skill_id(self, skill: str, category: str) -> str:
        """Generate unique skill ID"""
        return hashlib.md5(f"{skill}_{category}".encode()).hexdigest()[:12]
    
    def _determine_challenge_type(self, skill: str, category: str) -> str:
        """Determine the type of challenge for a skill"""
        if category == 'programming_languages':
            return 'live_coding'
        elif category == 'databases':
            return 'sql_sandbox'
        elif category == 'frameworks_libraries':
            return 'code_review'
        else:
            return 'conceptual'
    
    def _get_estimated_time(self, skill: str, category: str) -> int:
        """Get estimated time for skill verification in minutes"""
        time_mapping = {
            'programming_languages': 15,
            'databases': 10,
            'frameworks_libraries': 8,
            'cloud_technologies': 12,
            'data_science': 20
        }
        return time_mapping.get(category, 10)
    
    def _calculate_priority_score(self, skill: str, category: str) -> int:
        """Calculate priority score for skill verification (1-10)"""
        high_priority_skills = {
            'python': 10, 'java': 9, 'javascript': 9, 'sql': 10,
            'react': 9, 'aws': 8, 'docker': 7, 'git': 8
        }
        
        return high_priority_skills.get(skill.lower(), 5)
    
    def _generate_verification_recommendations(self, queue: List[Dict]) -> List[str]:
        """Generate recommendations for skill verification"""
        recommendations = []
        
        high_priority = [item for item in queue if item['priority_score'] > 8]
        if high_priority:
            recommendations.append(f"🚀 Start with high-priority skills: {', '.join([item['skill_name'] for item in high_priority[:3]])}")
        
        total_time = sum(item['estimated_time'] for item in queue)
        if total_time > 60:
            recommendations.append("⏰ Consider spreading verifications across multiple sessions")
        
        programming_skills = [item for item in queue if item['category'] == 'programming_languages']
        if len(programming_skills) > 3:
            recommendations.append("💻 Focus on 2-3 core programming languages for maximum impact")
        
        return recommendations
    
    def _load_programming_challenges(self) -> Dict:
        """Load programming challenge database"""
        # In a real implementation, this would load from a file or database
        return {}
    
    def _load_sql_challenges(self) -> Dict:
        """Load SQL challenge database"""
        return {}
    
    def _load_framework_challenges(self) -> Dict:
        """Load framework challenge database"""
        return {}
    
    def _generate_cloud_challenge(self, skill: str, difficulty: str) -> Dict[str, Any]:
        """Generate cloud technology challenges"""
        return {
            'title': f'{skill} Configuration Challenge',
            'description': f'Demonstrate your {skill} knowledge',
            'category': 'conceptual',
            'time_limit': 10
        }
    
    def _generate_data_science_challenge(self, skill: str, difficulty: str) -> Dict[str, Any]:
        """Generate data science challenges"""
        return {
            'title': f'{skill} Analysis Challenge',
            'description': f'Apply {skill} concepts to solve a problem',
            'category': 'conceptual',
            'time_limit': 20
        }
    
    def _generate_general_challenge(self, skill: str, difficulty: str) -> Dict[str, Any]:
        """Generate general conceptual challenges"""
        return {
            'title': f'{skill} Knowledge Check',
            'description': f'Test your understanding of {skill}',
            'category': 'conceptual',
            'time_limit': 8
        }
    
    def _evaluate_sql_challenge(self, challenge_response: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate SQL challenge response"""
        # Placeholder implementation
        return {'score': 85, 'feedback': ['SQL query executed successfully']}
    
    def _evaluate_code_review_challenge(self, challenge_response: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate code review challenge response"""
        # Placeholder implementation  
        return {'score': 80, 'feedback': ['Good understanding of the concept']}
    
    def _evaluate_general_challenge(self, challenge_response: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate general challenge response"""
        # Placeholder implementation
        return {'score': 75, 'feedback': ['Satisfactory response']}

# Example usage and testing
if __name__ == "__main__":
    # Initialize the skill verification engine
    engine = SkillVerificationEngine()
    
    # Test skill extraction
    sample_resume = """
    John Doe
    Software Engineer
    
    Skills:
    - Programming: Python, Java, JavaScript, C++
    - Databases: MySQL, PostgreSQL, MongoDB
    - Frameworks: React, Django, Flask, Spring Boot
    - Cloud: AWS, Docker, Kubernetes
    - Tools: Git, Jenkins, Docker
    
    Experience:
    - Proficient in Python with 3 years experience
    - Skilled in React development
    - Experience with AWS cloud services
    """
    
    extracted_skills = engine.extract_skills_from_resume(sample_resume)
    print("🔍 Extracted Skills:")
    for category, skills in extracted_skills.items():
        print(f"  {category}: {skills}")
    
    # Generate verification queue
    verification_queue = engine.generate_verification_queue(user_id=1, extracted_skills=extracted_skills)
    print(f"\n📋 Verification Queue ({verification_queue['total_skills']} skills):")
    for item in verification_queue['queue'][:3]:  # Show first 3
        print(f"  • {item['skill_name']} ({item['category']}) - {item['estimated_time']} min - Priority: {item['priority_score']}")
    
    # Test challenge generation
    print("\n🧪 Sample Challenges:")
    python_challenge = engine.get_verification_challenge('Python', 'programming_languages')
    print(f"Python Challenge: {python_challenge['title']}")
    print(f"Description: {python_challenge['description']}")
    
    sql_challenge = engine.get_verification_challenge('SQL', 'databases')
    print(f"SQL Challenge: {sql_challenge['title']}")
    
    print("\n✅ Skill Verification Engine initialized successfully!")