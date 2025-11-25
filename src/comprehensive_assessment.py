"""
Comprehensive Assessment Module for Placement Prediction System
Includes Aptitude Tests, Cognitive Tests, and Advanced Analytics
"""

import json
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import numpy as np
import pandas as pd

class ComprehensiveAssessmentEngine:
    """
    Advanced assessment engine for aptitude, cognitive, and skill evaluation
    """
    
    def __init__(self):
        self.question_bank = self._load_question_bank()
        self.assessment_types = {
            'logical_reasoning': 'Logical Reasoning',
            'quantitative_aptitude': 'Quantitative Aptitude', 
            'data_interpretation': 'Data Interpretation',
            'verbal_ability': 'Verbal Ability',
            'technical_concepts': 'Technical Concepts'
        }
        
    def _load_question_bank(self) -> Dict[str, List[Dict]]:
        """Load comprehensive question bank from JSON or create default"""
        default_questions = {
            "logical_reasoning": [
                {
                    "id": "lr_001",
                    "question": "If all roses are flowers and some flowers are red, which statement is definitely true?",
                    "options": [
                        "All roses are red",
                        "Some roses are red", 
                        "Some roses may be red",
                        "No roses are red"
                    ],
                    "correct_answer": 2,
                    "explanation": "We can only conclude that some roses may be red, not definitely.",
                    "difficulty": "medium",
                    "topic": "syllogisms",
                    "time_limit": 60
                },
                {
                    "id": "lr_002",
                    "question": "In a certain code, 'COMPUTER' is written as 'RFUVQNPC'. How is 'MONITOR' written?",
                    "options": [
                        "SRMFGLU",
                        "SRNFGLU", 
                        "SRMGFLU",
                        "SRNFGKP"
                    ],
                    "correct_answer": 1,
                    "explanation": "Each letter is shifted by +3 positions and then reversed.",
                    "difficulty": "hard",
                    "topic": "coding_decoding",
                    "time_limit": 90
                },
                {
                    "id": "lr_003",
                    "question": "Find the next number in the series: 2, 6, 12, 20, 30, ?",
                    "options": ["40", "42", "44", "46"],
                    "correct_answer": 1,
                    "explanation": "Pattern: n(n+1) where n = 1,2,3,4,5,6. Next is 6×7 = 42",
                    "difficulty": "easy",
                    "topic": "number_series",
                    "time_limit": 45
                }
            ],
            "quantitative_aptitude": [
                {
                    "id": "qa_001",
                    "question": "A train 120m long running at 60 km/hr takes how long to cross a platform 180m long?",
                    "options": ["15 seconds", "18 seconds", "20 seconds", "25 seconds"],
                    "correct_answer": 1,
                    "explanation": "Total distance = 120+180 = 300m. Speed = 60×5/18 = 16.67 m/s. Time = 300/16.67 = 18 seconds",
                    "difficulty": "medium", 
                    "topic": "time_speed_distance",
                    "time_limit": 120
                },
                {
                    "id": "qa_002",
                    "question": "If the compound interest on Rs. 1000 for 2 years at 10% per annum is Rs. 210, what is the simple interest?",
                    "options": ["Rs. 180", "Rs. 200", "Rs. 220", "Rs. 240"],
                    "correct_answer": 1,
                    "explanation": "SI for 2 years = P×R×T/100 = 1000×10×2/100 = Rs. 200",
                    "difficulty": "medium",
                    "topic": "simple_compound_interest",
                    "time_limit": 90
                },
                {
                    "id": "qa_003",
                    "question": "In how many ways can 5 people be arranged in a row?",
                    "options": ["100", "120", "150", "200"],
                    "correct_answer": 1,
                    "explanation": "5! = 5×4×3×2×1 = 120 ways",
                    "difficulty": "easy",
                    "topic": "permutation_combination",
                    "time_limit": 60
                }
            ],
            "data_interpretation": [
                {
                    "id": "di_001",
                    "question": "Based on the sales data: Q1: 100, Q2: 150, Q3: 120, Q4: 180. What is the percentage increase from Q1 to Q4?",
                    "options": ["60%", "70%", "80%", "90%"],
                    "correct_answer": 2,
                    "explanation": "Increase = (180-100)/100 × 100 = 80%",
                    "difficulty": "easy",
                    "topic": "percentage_analysis",
                    "time_limit": 90
                },
                {
                    "id": "di_002",
                    "question": "A company's revenue grew from $1M to $1.5M. If the growth rate remains constant, what will be the revenue after one more period?",
                    "options": ["$2.0M", "$2.25M", "$2.5M", "$3.0M"],
                    "correct_answer": 1,
                    "explanation": "Growth rate = 50%. Next period: 1.5 × 1.5 = $2.25M",
                    "difficulty": "medium",
                    "topic": "growth_analysis",
                    "time_limit": 120
                }
            ],
            "verbal_ability": [
                {
                    "id": "va_001",
                    "question": "Choose the word most similar in meaning to 'METICULOUS':",
                    "options": ["Careless", "Thorough", "Quick", "Simple"],
                    "correct_answer": 1,
                    "explanation": "Meticulous means very careful and precise, similar to thorough.",
                    "difficulty": "medium",
                    "topic": "synonyms",
                    "time_limit": 30
                },
                {
                    "id": "va_002", 
                    "question": "Identify the error in: 'Each of the students have submitted their assignment.'",
                    "options": [
                        "No error",
                        "'have' should be 'has'",
                        "'their' should be 'his/her'", 
                        "Both B and C"
                    ],
                    "correct_answer": 3,
                    "explanation": "'Each' is singular, so 'have' should be 'has' and 'their' should be 'his/her'.",
                    "difficulty": "hard",
                    "topic": "grammar",
                    "time_limit": 60
                }
            ],
            "technical_concepts": [
                {
                    "id": "tc_001",
                    "question": "What is the time complexity of binary search?",
                    "options": ["O(n)", "O(log n)", "O(n log n)", "O(n²)"],
                    "correct_answer": 1,
                    "explanation": "Binary search eliminates half the search space in each iteration, resulting in O(log n) complexity.",
                    "difficulty": "easy",
                    "topic": "algorithms",
                    "time_limit": 45
                },
                {
                    "id": "tc_002",
                    "question": "Which design pattern ensures a class has only one instance?",
                    "options": ["Factory", "Observer", "Singleton", "Strategy"],
                    "correct_answer": 2,
                    "explanation": "Singleton pattern restricts instantiation of a class to one single instance.",
                    "difficulty": "medium",
                    "topic": "design_patterns",
                    "time_limit": 60
                }
            ]
        }
        
        return default_questions
    
    def generate_adaptive_test(self, assessment_type: str, difficulty_level: str = "mixed", 
                              num_questions: int = 10) -> Dict[str, Any]:
        """
        Generate adaptive test based on user performance and requirements
        """
        if assessment_type not in self.question_bank:
            raise ValueError(f"Assessment type '{assessment_type}' not supported")
        
        questions = self.question_bank[assessment_type]
        
        # Filter by difficulty if specified
        if difficulty_level != "mixed":
            questions = [q for q in questions if q.get('difficulty') == difficulty_level]
        
        # Select questions (ensuring variety in topics)
        selected_questions = self._select_diverse_questions(questions, num_questions)
        
        test_config = {
            'test_id': f"{assessment_type}_{int(time.time())}",
            'assessment_type': assessment_type,
            'title': self.assessment_types[assessment_type],
            'questions': selected_questions,
            'total_questions': len(selected_questions),
            'total_time': sum(q.get('time_limit', 60) for q in selected_questions),
            'instructions': self._get_test_instructions(assessment_type),
            'scoring_method': 'weighted',  # Based on difficulty
            'negative_marking': True,
            'negative_marking_ratio': 0.25
        }
        
        return test_config
    
    def _select_diverse_questions(self, questions: List[Dict], num_questions: int) -> List[Dict]:
        """Select questions ensuring topic diversity"""
        if len(questions) <= num_questions:
            return questions
        
        # Group by topic for diversity
        topics = {}
        for q in questions:
            topic = q.get('topic', 'general')
            if topic not in topics:
                topics[topic] = []
            topics[topic].append(q)
        
        # Select questions with topic diversity
        selected = []
        topic_names = list(topics.keys())
        
        for i in range(num_questions):
            topic = topic_names[i % len(topic_names)]
            if topics[topic]:
                selected.append(topics[topic].pop(0))
        
        return selected
    
    def _get_test_instructions(self, assessment_type: str) -> List[str]:
        """Get specific instructions for each assessment type"""
        instructions = {
            'logical_reasoning': [
                "This section tests your logical thinking and reasoning abilities.",
                "Read each question carefully and select the best answer.",
                "Some questions may have multiple valid approaches - choose the most logical one.",
                "Negative marking: -0.25 for incorrect answers."
            ],
            'quantitative_aptitude': [
                "This section tests your mathematical and numerical abilities.",
                "You may use rough calculations, but be precise in your final answer.",
                "Manage your time wisely - some problems may take longer than others.",
                "Negative marking: -0.25 for incorrect answers."
            ],
            'data_interpretation': [
                "This section tests your ability to analyze and interpret data.",
                "Pay attention to units, scales, and trends in the data.",
                "Calculate carefully and double-check your arithmetic.",
                "Negative marking: -0.25 for incorrect answers."
            ],
            'verbal_ability': [
                "This section tests your English language proficiency.",
                "Focus on grammar, vocabulary, and comprehension.",
                "Read questions carefully - attention to detail is crucial.",
                "Negative marking: -0.25 for incorrect answers."
            ],
            'technical_concepts': [
                "This section tests your technical knowledge and concepts.",
                "Apply fundamental concepts to solve problems.",
                "Think about real-world applications of theoretical concepts.",
                "Negative marking: -0.25 for incorrect answers."
            ]
        }
        
        return instructions.get(assessment_type, ["General assessment instructions."])
    
    def evaluate_test_performance(self, test_config: Dict, user_responses: List[Dict]) -> Dict[str, Any]:
        """
        Comprehensive evaluation with detailed analytics
        """
        questions = test_config['questions']
        total_questions = len(questions)
        
        # Initialize scoring variables
        correct_answers = 0
        incorrect_answers = 0
        unanswered = 0
        total_time_taken = 0
        topic_performance = {}
        difficulty_performance = {'easy': {'correct': 0, 'total': 0}, 
                                'medium': {'correct': 0, 'total': 0},
                                'hard': {'correct': 0, 'total': 0}}
        
        # Detailed analysis
        question_analysis = []
        
        for i, question in enumerate(questions):
            user_response = user_responses[i] if i < len(user_responses) else None
            
            question_result = {
                'question_id': question['id'],
                'topic': question.get('topic', 'general'),
                'difficulty': question.get('difficulty', 'medium'),
                'correct_answer': question['correct_answer'],
                'user_answer': user_response.get('answer') if user_response else None,
                'time_taken': user_response.get('time_taken', 0) if user_response else 0,
                'is_correct': False,
                'points_earned': 0
            }
            
            # Check correctness and calculate points
            if user_response and user_response.get('answer') is not None:
                if user_response['answer'] == question['correct_answer']:
                    question_result['is_correct'] = True
                    correct_answers += 1
                    
                    # Weighted scoring based on difficulty
                    difficulty_weights = {'easy': 1, 'medium': 2, 'hard': 3}
                    question_result['points_earned'] = difficulty_weights.get(question.get('difficulty', 'medium'), 2)
                else:
                    incorrect_answers += 1
                    # Negative marking
                    if test_config.get('negative_marking', True):
                        question_result['points_earned'] = -test_config.get('negative_marking_ratio', 0.25)
            else:
                unanswered += 1
            
            # Topic performance tracking
            topic = question.get('topic', 'general')
            if topic not in topic_performance:
                topic_performance[topic] = {'correct': 0, 'total': 0, 'time_spent': 0}
            
            topic_performance[topic]['total'] += 1
            topic_performance[topic]['time_spent'] += question_result['time_taken']
            if question_result['is_correct']:
                topic_performance[topic]['correct'] += 1
            
            # Difficulty performance tracking
            diff = question.get('difficulty', 'medium')
            difficulty_performance[diff]['total'] += 1
            if question_result['is_correct']:
                difficulty_performance[diff]['correct'] += 1
            
            total_time_taken += question_result['time_taken']
            question_analysis.append(question_result)
        
        # Calculate scores and percentages
        raw_score = sum(q['points_earned'] for q in question_analysis)
        max_possible_score = sum(2 if q.get('difficulty') == 'medium' else 
                               (3 if q.get('difficulty') == 'hard' else 1) 
                               for q in questions)
        
        percentage_score = max(0, (raw_score / max_possible_score) * 100) if max_possible_score > 0 else 0
        accuracy = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        
        # Performance analysis
        weak_topics = [topic for topic, perf in topic_performance.items() 
                      if perf['total'] > 0 and (perf['correct'] / perf['total']) < 0.6]
        
        strong_topics = [topic for topic, perf in topic_performance.items() 
                        if perf['total'] > 0 and (perf['correct'] / perf['total']) >= 0.8]
        
        # Generate insights and recommendations
        insights = self._generate_performance_insights(
            topic_performance, difficulty_performance, 
            total_time_taken, test_config['total_time']
        )
        
        # Calculate proficiency level
        proficiency_level = self._calculate_proficiency_level(percentage_score, accuracy)
        
        return {
            'test_id': test_config['test_id'],
            'assessment_type': test_config['assessment_type'],
            'completion_timestamp': datetime.now().isoformat(),
            
            # Overall scores
            'raw_score': raw_score,
            'max_possible_score': max_possible_score,
            'percentage_score': round(percentage_score, 2),
            'accuracy': round(accuracy, 2),
            'proficiency_level': proficiency_level,
            
            # Answer statistics
            'correct_answers': correct_answers,
            'incorrect_answers': incorrect_answers,
            'unanswered': unanswered,
            'total_questions': total_questions,
            
            # Time analysis
            'total_time_taken': total_time_taken,
            'time_efficiency': round((test_config['total_time'] - total_time_taken) / test_config['total_time'] * 100, 2),
            'average_time_per_question': round(total_time_taken / total_questions, 2) if total_questions > 0 else 0,
            
            # Detailed performance breakdown
            'topic_performance': {
                topic: {
                    'accuracy': round((perf['correct'] / perf['total']) * 100, 2) if perf['total'] > 0 else 0,
                    'questions_attempted': perf['total'],
                    'correct_answers': perf['correct'],
                    'avg_time_per_question': round(perf['time_spent'] / perf['total'], 2) if perf['total'] > 0 else 0
                }
                for topic, perf in topic_performance.items()
            },
            
            'difficulty_performance': {
                diff: {
                    'accuracy': round((perf['correct'] / perf['total']) * 100, 2) if perf['total'] > 0 else 0,
                    'questions_attempted': perf['total'],
                    'correct_answers': perf['correct']
                }
                for diff, perf in difficulty_performance.items()
            },
            
            # Insights and recommendations
            'weak_topics': weak_topics,
            'strong_topics': strong_topics,
            'insights': insights,
            'detailed_question_analysis': question_analysis,
            
            # Features for ML model
            'ml_features': self._extract_ml_features(
                topic_performance, difficulty_performance, 
                percentage_score, accuracy, total_time_taken, test_config
            )
        }
    
    def _generate_performance_insights(self, topic_performance: Dict, difficulty_performance: Dict,
                                     time_taken: int, total_time: int) -> List[str]:
        """Generate actionable insights based on performance"""
        insights = []
        
        # Time management insights
        time_efficiency = (total_time - time_taken) / total_time
        if time_efficiency < 0:
            insights.append("⏰ Time Management: You exceeded the time limit. Practice solving questions faster.")
        elif time_efficiency > 0.3:
            insights.append("⚡ Time Management: Great! You completed the test well within time. You can afford to double-check answers.")
        
        # Difficulty analysis
        easy_acc = difficulty_performance['easy']['correct'] / max(1, difficulty_performance['easy']['total'])
        hard_acc = difficulty_performance['hard']['correct'] / max(1, difficulty_performance['hard']['total'])
        
        if easy_acc < 0.8:
            insights.append("📚 Foundation: Focus on strengthening basic concepts before attempting harder problems.")
        
        if hard_acc > 0.6 and easy_acc > 0.8:
            insights.append("🎯 Advanced Level: Excellent problem-solving skills! You're ready for challenging assessments.")
        
        # Topic-specific insights
        weak_topics = [topic for topic, perf in topic_performance.items() 
                      if perf['total'] > 0 and (perf['correct'] / perf['total']) < 0.5]
        
        if weak_topics:
            insights.append(f"📖 Study Focus: Need improvement in: {', '.join(weak_topics)}")
        
        return insights
    
    def _calculate_proficiency_level(self, percentage_score: float, accuracy: float) -> str:
        """Calculate overall proficiency level"""
        avg_score = (percentage_score + accuracy) / 2
        
        if avg_score >= 85:
            return "Expert"
        elif avg_score >= 70:
            return "Advanced"
        elif avg_score >= 55:
            return "Intermediate"
        elif avg_score >= 40:
            return "Beginner"
        else:
            return "Needs Improvement"
    
    def _extract_ml_features(self, topic_performance: Dict, difficulty_performance: Dict,
                           percentage_score: float, accuracy: float, time_taken: int,
                           test_config: Dict) -> Dict[str, float]:
        """Extract features that can be used in the placement prediction ML model"""
        features = {
            f"{test_config['assessment_type']}_score": percentage_score,
            f"{test_config['assessment_type']}_accuracy": accuracy,
            f"{test_config['assessment_type']}_time_efficiency": (test_config['total_time'] - time_taken) / test_config['total_time'] * 100,
            f"{test_config['assessment_type']}_easy_accuracy": (difficulty_performance['easy']['correct'] / max(1, difficulty_performance['easy']['total'])) * 100,
            f"{test_config['assessment_type']}_medium_accuracy": (difficulty_performance['medium']['correct'] / max(1, difficulty_performance['medium']['total'])) * 100,
            f"{test_config['assessment_type']}_hard_accuracy": (difficulty_performance['hard']['correct'] / max(1, difficulty_performance['hard']['total'])) * 100,
        }
        
        # Add topic-specific features
        for topic, perf in topic_performance.items():
            topic_accuracy = (perf['correct'] / perf['total']) * 100 if perf['total'] > 0 else 0
            features[f"{test_config['assessment_type']}_{topic}_accuracy"] = topic_accuracy
        
        return features
    
    def get_improvement_recommendations(self, assessment_results: Dict) -> List[Dict[str, str]]:
        """Generate specific improvement recommendations based on assessment results"""
        recommendations = []
        
        weak_topics = assessment_results.get('weak_topics', [])
        assessment_type = assessment_results.get('assessment_type', '')
        accuracy = assessment_results.get('accuracy', 0)
        
        # Topic-specific recommendations
        topic_recommendations = {
            'syllogisms': {
                'study_material': 'Practice Venn diagrams and logical deduction exercises',
                'recommended_courses': ['Logical Reasoning Fundamentals', 'Critical Thinking']
            },
            'coding_decoding': {
                'study_material': 'Pattern recognition and alphabetical/numerical sequences',
                'recommended_courses': ['Aptitude Test Preparation', 'Pattern Analysis']
            },
            'number_series': {
                'study_material': 'Mathematical patterns and sequence formulas',
                'recommended_courses': ['Mathematical Reasoning', 'Number Theory Basics']
            },
            'time_speed_distance': {
                'study_material': 'Practice formula application and unit conversions',
                'recommended_courses': ['Quantitative Aptitude', 'Physics for Aptitude']
            },
            'permutation_combination': {
                'study_material': 'Combinatorics principles and formula derivations',
                'recommended_courses': ['Discrete Mathematics', 'Probability & Statistics']
            },
            'algorithms': {
                'study_material': 'Data structures and algorithm complexity analysis',
                'recommended_courses': ['DSA Fundamentals', 'Competitive Programming']
            }
        }
        
        for topic in weak_topics:
            if topic in topic_recommendations:
                recommendations.append({
                    'type': 'topic_improvement',
                    'topic': topic,
                    'priority': 'high',
                    'study_material': topic_recommendations[topic]['study_material'],
                    'recommended_courses': topic_recommendations[topic]['recommended_courses']
                })
        
        # General recommendations based on overall performance
        if accuracy < 50:
            recommendations.append({
                'type': 'foundation_building',
                'priority': 'critical',
                'recommendation': 'Focus on building strong fundamentals before attempting advanced topics',
                'suggested_action': 'Take easier practice tests and gradually increase difficulty'
            })
        elif accuracy < 70:
            recommendations.append({
                'type': 'skill_enhancement',
                'priority': 'high', 
                'recommendation': 'Good foundation, but need more practice for consistency',
                'suggested_action': 'Regular practice with timed tests and detailed analysis'
            })
        
        return recommendations

def main():
    """Test the comprehensive assessment engine"""
    print("🧠 Testing Comprehensive Assessment Engine")
    print("=" * 50)
    
    engine = ComprehensiveAssessmentEngine()
    
    # Generate a sample test
    test_config = engine.generate_adaptive_test('logical_reasoning', num_questions=5)
    print(f"Generated test: {test_config['title']}")
    print(f"Questions: {test_config['total_questions']}")
    print(f"Total time: {test_config['total_time']} seconds")
    
    # Simulate user responses
    sample_responses = [
        {'answer': 2, 'time_taken': 45},
        {'answer': 1, 'time_taken': 60},
        {'answer': 0, 'time_taken': 30},  # Wrong answer
        {'answer': None, 'time_taken': 0},  # Unanswered
        {'answer': 1, 'time_taken': 40}
    ]
    
    # Evaluate performance
    results = engine.evaluate_test_performance(test_config, sample_responses)
    
    print(f"\nTest Results:")
    print(f"Score: {results['percentage_score']:.1f}%")
    print(f"Accuracy: {results['accuracy']:.1f}%")
    print(f"Proficiency: {results['proficiency_level']}")
    print(f"Weak topics: {results['weak_topics']}")
    print(f"Insights: {results['insights']}")
    
    # Get recommendations
    recommendations = engine.get_improvement_recommendations(results)
    print(f"\nRecommendations: {len(recommendations)} items")
    
    print("\n✅ Comprehensive Assessment Engine test completed!")

if __name__ == "__main__":
    main()