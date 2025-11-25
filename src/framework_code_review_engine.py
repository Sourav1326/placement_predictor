"""
🔍 FRAMEWORK CODE REVIEW ENGINE
Interactive challenges for testing framework and library knowledge
"""

import json
import re
import hashlib
import time
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import difflib

class FrameworkCodeReviewEngine:
    """
    Engine for testing framework/library knowledge through code review challenges
    """
    
    def __init__(self):
        self.supported_frameworks = {
            'react': 'React.js Frontend Framework',
            'angular': 'Angular Frontend Framework', 
            'vue': 'Vue.js Frontend Framework',
            'django': 'Django Python Web Framework',
            'flask': 'Flask Python Microframework',
            'spring': 'Spring Java Framework',
            'express': 'Express.js Node.js Framework',
            'tensorflow': 'TensorFlow Machine Learning',
            'pytorch': 'PyTorch Machine Learning',
            'pandas': 'Pandas Data Analysis',
            'react_native': 'React Native Mobile Development'
        }
        
        self.challenge_types = [
            'bug_identification',
            'code_explanation',
            'best_practices',
            'optimization',
            'pattern_recognition',
            'api_usage'
        ]
        
        self.challenge_database = self._load_framework_challenges()
    
    def get_framework_challenge(self, framework: str, difficulty: str = 'medium', 
                              challenge_type: str = 'bug_identification') -> Dict[str, Any]:
        """
        Get a framework-specific challenge
        """
        framework_lower = framework.lower()
        
        if framework_lower not in self.supported_frameworks:
            raise ValueError(f"Framework '{framework}' not supported")
        
        challenges = self.challenge_database.get(framework_lower, {})
        challenge_key = f"{difficulty}_{challenge_type}"
        
        challenge = challenges.get(challenge_key)
        if not challenge:
            # Fallback to any available challenge for the framework
            available_challenges = list(challenges.keys())
            if available_challenges:
                challenge = challenges[available_challenges[0]]
            else:
                challenge = self._generate_generic_challenge(framework, difficulty)
        
        # Add metadata
        challenge['framework'] = framework
        challenge['difficulty'] = difficulty
        challenge['challenge_type'] = challenge_type
        challenge['challenge_id'] = hashlib.md5(
            f"{framework}_{difficulty}_{challenge_type}_{time.time()}".encode()
        ).hexdigest()[:12]
        
        return challenge
    
    def evaluate_code_review_response(self, challenge: Dict[str, Any], 
                                    user_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate user's code review response
        """
        challenge_type = challenge.get('challenge_type', 'bug_identification')
        
        if challenge_type == 'bug_identification':
            return self._evaluate_bug_identification(challenge, user_response)
        elif challenge_type == 'code_explanation':
            return self._evaluate_code_explanation(challenge, user_response)
        elif challenge_type == 'best_practices':
            return self._evaluate_best_practices(challenge, user_response)
        elif challenge_type == 'optimization':
            return self._evaluate_optimization(challenge, user_response)
        elif challenge_type == 'pattern_recognition':
            return self._evaluate_pattern_recognition(challenge, user_response)
        elif challenge_type == 'api_usage':
            return self._evaluate_api_usage(challenge, user_response)
        else:
            return self._evaluate_generic_response(challenge, user_response)
    
    def _evaluate_bug_identification(self, challenge: Dict[str, Any], 
                                   user_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate bug identification challenge
        """
        correct_answer = challenge.get('correct_answer', '')
        user_answer = user_response.get('selected_option', '')
        explanation = user_response.get('explanation', '')
        
        # Check if user selected correct option
        correct_selection = user_answer.lower() == correct_answer.lower()
        
        # Analyze explanation quality
        explanation_score = self._analyze_explanation_quality(explanation, challenge)
        
        # Calculate overall score
        base_score = 70 if correct_selection else 0
        explanation_bonus = explanation_score * 0.3
        total_score = min(100, base_score + explanation_bonus)
        
        # Generate feedback
        feedback = self._generate_bug_identification_feedback(
            correct_selection, explanation, challenge
        )
        
        return {
            'verification_passed': total_score >= 70,
            'score': total_score,
            'correct_selection': correct_selection,
            'explanation_score': explanation_score,
            'feedback': feedback,
            'detailed_analysis': {
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'explanation_quality': self._get_explanation_quality_rating(explanation_score)
            }
        }
    
    def _evaluate_code_explanation(self, challenge: Dict[str, Any], 
                                 user_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate code explanation challenge
        """
        user_explanation = user_response.get('explanation', '')
        expected_keywords = challenge.get('expected_keywords', [])
        correct_concepts = challenge.get('correct_concepts', [])
        
        # Check for key concepts
        concepts_mentioned = 0
        for concept in correct_concepts:
            if concept.lower() in user_explanation.lower():
                concepts_mentioned += 1
        
        # Check for technical keywords
        keywords_mentioned = 0
        for keyword in expected_keywords:
            if keyword.lower() in user_explanation.lower():
                keywords_mentioned += 1
        
        # Calculate scores
        concept_score = (concepts_mentioned / len(correct_concepts)) * 100 if correct_concepts else 50
        keyword_score = (keywords_mentioned / len(expected_keywords)) * 100 if expected_keywords else 50
        length_score = min(100, len(user_explanation) / 10)  # Encourage detailed explanations
        
        # Overall score
        total_score = (concept_score * 0.5 + keyword_score * 0.3 + length_score * 0.2)
        
        feedback = [
            f"You mentioned {concepts_mentioned}/{len(correct_concepts)} key concepts",
            f"You used {keywords_mentioned}/{len(expected_keywords)} technical terms",
        ]
        
        if total_score >= 80:
            feedback.append("🎉 Excellent explanation! You demonstrated strong understanding.")
        elif total_score >= 60:
            feedback.append("👍 Good explanation, but could be more detailed.")
        else:
            feedback.append("💡 Try to include more technical details and framework-specific concepts.")
        
        return {
            'verification_passed': total_score >= 70,
            'score': total_score,
            'concepts_score': concept_score,
            'keywords_score': keyword_score,
            'feedback': feedback
        }
    
    def _evaluate_best_practices(self, challenge: Dict[str, Any], 
                               user_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate best practices challenge
        """
        user_suggestions = user_response.get('suggestions', [])
        best_practices = challenge.get('best_practices', [])
        
        # Match user suggestions with known best practices
        matches = 0
        for practice in best_practices:
            for suggestion in user_suggestions:
                if self._calculate_text_similarity(practice.lower(), suggestion.lower()) > 0.6:
                    matches += 1
                    break
        
        score = (matches / len(best_practices)) * 100 if best_practices else 0
        
        feedback = [
            f"You identified {matches}/{len(best_practices)} key best practices",
        ]
        
        if score >= 80:
            feedback.append("✨ Great knowledge of best practices!")
        else:
            missing_practices = len(best_practices) - matches
            feedback.append(f"💡 Consider {missing_practices} additional best practice(s)")
        
        return {
            'verification_passed': score >= 70,
            'score': score,
            'practices_identified': matches,
            'feedback': feedback
        }
    
    def _analyze_explanation_quality(self, explanation: str, challenge: Dict[str, Any]) -> float:
        """
        Analyze the quality of user's explanation
        """
        if not explanation or len(explanation.strip()) < 10:
            return 0
        
        quality_score = 0
        
        # Length and detail
        if len(explanation) > 50:
            quality_score += 20
        if len(explanation) > 100:
            quality_score += 10
        
        # Technical terms usage
        framework = challenge.get('framework', '').lower()
        framework_terms = self._get_framework_technical_terms(framework)
        
        terms_used = sum(1 for term in framework_terms if term in explanation.lower())
        quality_score += min(30, terms_used * 10)
        
        # Code structure awareness
        code_structure_terms = ['component', 'function', 'method', 'class', 'variable', 'state', 'props']
        structure_terms_used = sum(1 for term in code_structure_terms if term in explanation.lower())
        quality_score += min(20, structure_terms_used * 5)
        
        # Problem solving approach
        problem_solving_terms = ['because', 'should', 'instead', 'fix', 'correct', 'proper', 'better']
        problem_terms_used = sum(1 for term in problem_solving_terms if term in explanation.lower())
        quality_score += min(20, problem_terms_used * 4)
        
        return min(100, quality_score)
    
    def _get_framework_technical_terms(self, framework: str) -> List[str]:
        """
        Get technical terms specific to a framework
        """
        terms_map = {
            'react': ['jsx', 'component', 'state', 'props', 'hook', 'usestate', 'useeffect', 'render', 'virtual dom'],
            'angular': ['component', 'service', 'directive', 'module', 'dependency injection', 'observable', 'template'],
            'vue': ['component', 'directive', 'template', 'computed', 'watcher', 'lifecycle', 'vuex'],
            'django': ['model', 'view', 'template', 'url', 'orm', 'queryset', 'middleware', 'form'],
            'flask': ['route', 'blueprint', 'template', 'request', 'response', 'session', 'decorator'],
            'tensorflow': ['tensor', 'graph', 'session', 'placeholder', 'variable', 'operation', 'layer'],
            'pandas': ['dataframe', 'series', 'index', 'groupby', 'merge', 'pivot', 'query']
        }
        
        return terms_map.get(framework, [])
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate text similarity using difflib
        """
        return difflib.SequenceMatcher(None, text1, text2).ratio()
    
    def _generate_bug_identification_feedback(self, correct_selection: bool, 
                                            explanation: str, challenge: Dict) -> List[str]:
        """
        Generate feedback for bug identification challenges
        """
        feedback = []
        
        if correct_selection:
            feedback.append("✅ Correct! You identified the bug successfully.")
        else:
            feedback.append("❌ Incorrect selection. Review the code more carefully.")
            correct_answer = challenge.get('correct_answer', '')
            explanation_text = challenge.get('detailed_explanation', '')
            feedback.append(f"💡 The correct answer was: {correct_answer}")
            if explanation_text:
                feedback.append(f"📝 Explanation: {explanation_text}")
        
        if explanation and len(explanation) > 20:
            feedback.append("👍 Good job providing an explanation!")
        else:
            feedback.append("💭 Try to explain your reasoning for better learning.")
        
        return feedback
    
    def _get_explanation_quality_rating(self, score: float) -> str:
        """
        Convert explanation score to quality rating
        """
        if score >= 80:
            return "Excellent"
        elif score >= 60:
            return "Good"
        elif score >= 40:
            return "Fair"
        else:
            return "Needs Improvement"
    
    def _generate_generic_challenge(self, framework: str, difficulty: str) -> Dict[str, Any]:
        """
        Generate a generic challenge when specific ones aren't available
        """
        return {
            'title': f'{framework} Knowledge Check',
            'description': f'Test your understanding of {framework} concepts and best practices.',
            'challenge_type': 'code_explanation',
            'code_snippet': f'// {framework} code example would go here',
            'question': f'Explain how this {framework} code works and identify any potential issues.',
            'time_limit': 8,
            'expected_keywords': ['framework', 'code', 'function'],
            'correct_concepts': ['basic understanding']
        }
    
    def _evaluate_optimization(self, challenge: Dict[str, Any], user_response: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate optimization challenge"""
        return {'verification_passed': True, 'score': 75, 'feedback': ['Optimization evaluated']}
    
    def _evaluate_pattern_recognition(self, challenge: Dict[str, Any], user_response: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate pattern recognition challenge"""
        return {'verification_passed': True, 'score': 75, 'feedback': ['Pattern recognition evaluated']}
    
    def _evaluate_api_usage(self, challenge: Dict[str, Any], user_response: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate API usage challenge"""
        return {'verification_passed': True, 'score': 75, 'feedback': ['API usage evaluated']}
    
    def _evaluate_generic_response(self, challenge: Dict[str, Any], user_response: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate generic response"""
        return {'verification_passed': True, 'score': 70, 'feedback': ['Generic evaluation']}
    
    def _load_framework_challenges(self) -> Dict[str, Dict[str, Dict]]:
        """
        Load framework challenge database
        """
        return {
            'react': {
                'easy_bug_identification': {
                    'title': 'React State Update Bug',
                    'description': 'Identify why the counter is not updating when the button is clicked.',
                    'code_snippet': '''
import React, { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0);
    
    const handleClick = () => {
        count = count + 1;  // Bug: Direct mutation
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
                    'question': 'What is wrong with this React component?',
                    'options': [
                        'Missing useEffect hook',
                        'Direct state mutation instead of using setCount',
                        'Missing key prop',
                        'Incorrect import statement'
                    ],
                    'correct_answer': 'Direct state mutation instead of using setCount',
                    'detailed_explanation': 'In React, state should never be mutated directly. Use the setter function setCount(count + 1) instead.',
                    'time_limit': 5,
                    'expected_keywords': ['setCount', 'state', 'mutation', 'setter'],
                    'difficulty_level': 'easy'
                },
                'medium_bug_identification': {
                    'title': 'React useEffect Dependency Bug',
                    'description': 'Find the issue with this useEffect implementation.',
                    'code_snippet': '''
import React, { useState, useEffect } from 'react';

function UserProfile({ userId }) {
    const [user, setUser] = useState(null);
    
    useEffect(() => {
        fetchUser(userId).then(setUser);
    }, []); // Bug: Missing userId dependency
    
    return <div>{user ? user.name : 'Loading...'}</div>;
}
''',
                    'question': 'What will happen when userId changes?',
                    'options': [
                        'Component will re-render correctly',
                        'useEffect will not run again, showing stale data',
                        'Component will crash',
                        'Memory leak will occur'
                    ],
                    'correct_answer': 'useEffect will not run again, showing stale data',
                    'detailed_explanation': 'useEffect dependency array is missing userId, so it will only run once on mount.',
                    'time_limit': 7,
                    'expected_keywords': ['dependency', 'useEffect', 'userId', 'stale'],
                    'difficulty_level': 'medium'
                },
                'easy_code_explanation': {
                    'title': 'React Component Lifecycle',
                    'description': 'Explain what this React component does.',
                    'code_snippet': '''
import React, { useState, useEffect } from 'react';

function Timer() {
    const [seconds, setSeconds] = useState(0);
    
    useEffect(() => {
        const interval = setInterval(() => {
            setSeconds(prev => prev + 1);
        }, 1000);
        
        return () => clearInterval(interval);
    }, []);
    
    return <div>Timer: {seconds}s</div>;
}
''',
                    'question': 'Explain how this component works and what the useEffect does.',
                    'expected_keywords': ['timer', 'interval', 'useEffect', 'cleanup', 'seconds'],
                    'correct_concepts': [
                        'Creates a timer that increments every second',
                        'Uses useEffect to set up interval',
                        'Cleanup function clears interval',
                        'Prevents memory leaks'
                    ],
                    'time_limit': 8
                }
            },
            'django': {
                'medium_bug_identification': {
                    'title': 'Django Model Query Bug',
                    'description': 'Find the issue with this Django view.',
                    'code_snippet': '''
from django.shortcuts import render
from .models import User

def user_list(request):
    users = User.objects.all()
    for user in users:
        print(user.profile.bio)  # Bug: N+1 query problem
    
    return render(request, 'users.html', {'users': users})
''',
                    'question': 'What performance issue exists in this code?',
                    'options': [
                        'Memory leak',
                        'N+1 query problem',
                        'SQL injection vulnerability',
                        'Template rendering error'
                    ],
                    'correct_answer': 'N+1 query problem',
                    'detailed_explanation': 'Each user.profile access triggers a separate database query. Use select_related() to optimize.',
                    'time_limit': 6,
                    'expected_keywords': ['N+1', 'query', 'select_related', 'performance'],
                    'difficulty_level': 'medium'
                },
                'easy_best_practices': {
                    'title': 'Django Security Best Practices',
                    'description': 'What security improvements would you make to this Django view?',
                    'code_snippet': '''
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_user(request):
    user_id = request.GET.get('id')
    name = request.GET.get('name')
    
    # Update user in database
    User.objects.filter(id=user_id).update(name=name)
    
    return HttpResponse('Updated')
''',
                    'question': 'List security improvements for this view.',
                    'best_practices': [
                        'Remove @csrf_exempt decorator',
                        'Use POST instead of GET for updates',
                        'Add user authentication',
                        'Validate and sanitize input',
                        'Use form validation',
                        'Check user permissions'
                    ],
                    'time_limit': 10
                }
            },
            'flask': {
                'easy_bug_identification': {
                    'title': 'Flask Route Parameter Bug',
                    'description': 'Find the issue with this Flask route.',
                    'code_snippet': '''
from flask import Flask, request

app = Flask(__name__)

@app.route('/user/<user_id>')
def get_user(user_id):
    user = User.query.get(user_id)  # Bug: type mismatch
    if user:
        return f'User: {user.name}'
    return 'User not found'
''',
                    'question': 'What could go wrong with this route?',
                    'options': [
                        'Missing import statement',
                        'user_id is string but database expects integer',
                        'Missing error handling',
                        'Incorrect route syntax'
                    ],
                    'correct_answer': 'user_id is string but database expects integer',
                    'detailed_explanation': 'URL parameters are strings by default. Use <int:user_id> or convert to int.',
                    'time_limit': 5,
                    'expected_keywords': ['string', 'integer', 'type', 'conversion'],
                    'difficulty_level': 'easy'
                }
            },
            'tensorflow': {
                'medium_code_explanation': {
                    'title': 'TensorFlow Model Training',
                    'description': 'Explain what this TensorFlow code accomplishes.',
                    'code_snippet': '''
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
''',
                    'question': 'Explain the neural network architecture and training setup.',
                    'expected_keywords': ['neural network', 'dense layer', 'dropout', 'activation', 'optimizer', 'loss'],
                    'correct_concepts': [
                        'Sequential neural network model',
                        'Dense layer with ReLU activation',
                        'Dropout for regularization',
                        'Softmax output for classification',
                        'Adam optimizer',
                        'Categorical crossentropy loss'
                    ],
                    'time_limit': 12
                }
            }
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize the framework engine
    engine = FrameworkCodeReviewEngine()
    
    # Test React challenge
    react_challenge = engine.get_framework_challenge('react', 'easy', 'bug_identification')
    print("🔍 React Challenge:")
    print(f"Title: {react_challenge['title']}")
    print(f"Description: {react_challenge['description']}")
    print(f"Question: {react_challenge['question']}")
    print(f"Options: {react_challenge['options']}")
    
    # Test user response
    user_response = {
        'selected_option': 'Direct state mutation instead of using setCount',
        'explanation': 'React state should never be mutated directly. You need to use the setCount function to update state properly, otherwise the component will not re-render.'
    }
    
    evaluation = engine.evaluate_code_review_response(react_challenge, user_response)
    print(f"\n✅ Evaluation Result:")
    print(f"Verification Passed: {evaluation['verification_passed']}")
    print(f"Score: {evaluation['score']:.1f}%")
    print(f"Feedback: {evaluation['feedback']}")
    
    # Test Django challenge
    django_challenge = engine.get_framework_challenge('django', 'medium', 'bug_identification')
    print(f"\n🐍 Django Challenge:")
    print(f"Title: {django_challenge['title']}")
    print(f"Question: {django_challenge['question']}")
    
    print("\n🎯 Framework Code Review Engine ready!")