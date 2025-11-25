"""
Mock Interview Simulator with Real-time AI Feedback
Advanced interview practice system with behavioral and technical assessment
"""

import re
import random
from typing import Dict, List, Any, Tuple
from datetime import datetime

class MockInterviewEngine:
    """Advanced mock interview simulator with real-time AI feedback and STAR method analysis"""
    
    def __init__(self):
        self.question_bank = self._load_question_bank()
        self.evaluation_criteria = self._define_evaluation_criteria()
        self.star_method_keywords = self._load_star_keywords()
        
    def _load_question_bank(self) -> Dict[str, List[Dict]]:
        """Load comprehensive interview question bank"""
        return {
            "behavioral": [
                {
                    "id": "beh_001",
                    "question": "Tell me about yourself.",
                    "type": "introduction",
                    "expected_elements": ["background", "experience", "skills", "goals"],
                    "time_limit": 120,
                    "difficulty": "easy"
                },
                {
                    "id": "beh_002", 
                    "question": "Describe a challenging project you worked on and how you overcame the difficulties.",
                    "type": "problem_solving",
                    "expected_elements": ["situation", "task", "action", "result"],
                    "time_limit": 180,
                    "difficulty": "medium"
                },
                {
                    "id": "beh_003",
                    "question": "Tell me about a time when you had to work with a difficult team member.",
                    "type": "teamwork",
                    "expected_elements": ["situation", "task", "action", "result"],
                    "time_limit": 180,
                    "difficulty": "medium"
                },
                {
                    "id": "beh_004",
                    "question": "What is your biggest weakness?",
                    "type": "self_awareness",
                    "expected_elements": ["weakness", "awareness", "improvement_plan"],
                    "time_limit": 120,
                    "difficulty": "hard"
                }
            ],
            "technical": [
                {
                    "id": "tech_001",
                    "question": "Explain the difference between supervised and unsupervised machine learning.",
                    "type": "conceptual",
                    "expected_elements": ["definition", "examples", "use_cases"],
                    "time_limit": 180,
                    "difficulty": "medium"
                },
                {
                    "id": "tech_002",
                    "question": "How would you optimize a slow-running database query?",
                    "type": "problem_solving",
                    "expected_elements": ["analysis_approach", "optimization_techniques", "monitoring"],
                    "time_limit": 240,
                    "difficulty": "hard"
                }
            ]
        }
    
    def _define_evaluation_criteria(self) -> Dict[str, Dict]:
        """Define evaluation criteria for different aspects"""
        return {
            "content_quality": {"weight": 0.3},
            "communication_skills": {"weight": 0.25},
            "star_method_usage": {"weight": 0.2},
            "confidence_presence": {"weight": 0.15},
            "time_management": {"weight": 0.1}
        }
    
    def _load_star_keywords(self) -> Dict[str, List[str]]:
        """Load keywords that indicate STAR method components"""
        return {
            "situation": ["when", "there was", "situation", "context", "background", "at the time"],
            "task": ["needed to", "had to", "was responsible", "my goal", "objective", "required"],
            "action": ["i decided", "i took", "i implemented", "i created", "i developed", "i organized"],
            "result": ["resulted in", "outcome", "achieved", "successful", "improved", "increased"]
        }
    
    def generate_interview_session(self, interview_type: str = "mixed", duration_minutes: int = 30) -> Dict[str, Any]:
        """Generate a customized interview session"""
        
        num_questions = max(1, duration_minutes // 5)  # 5 minutes per question including feedback
        
        if interview_type == "mixed":
            selected_questions = []
            categories = list(self.question_bank.keys())
            
            for i in range(num_questions):
                category = categories[i % len(categories)]
                questions = self.question_bank[category]
                if questions:
                    selected_questions.append(random.choice(questions))
        else:
            if interview_type in self.question_bank:
                questions = self.question_bank[interview_type]
                selected_questions = random.sample(questions, min(num_questions, len(questions)))
            else:
                selected_questions = []
        
        return {
            'session_id': f"interview_{int(datetime.now().timestamp())}",
            'interview_type': interview_type,
            'duration_minutes': duration_minutes,
            'questions': selected_questions,
            'total_questions': len(selected_questions),
            'current_question_index': 0,
            'session_start_time': datetime.now().isoformat(),
            'instructions': self._get_interview_instructions(interview_type)
        }
    
    def _get_interview_instructions(self, interview_type: str) -> List[str]:
        """Get specific instructions for the interview type"""
        instructions = {
            "behavioral": [
                "🎯 Use the STAR method (Situation, Task, Action, Result) for your responses",
                "💡 Provide specific examples from your experience",
                "🗣️ Speak clearly and maintain good structure"
            ],
            "technical": [
                "🔧 Explain concepts clearly with examples when possible",
                "💭 Think out loud to show your reasoning process",
                "❓ Ask clarifying questions if needed"
            ],
            "mixed": [
                "📋 Use STAR method for behavioral questions",
                "🔧 Explain technical concepts clearly",
                "💡 Provide specific examples and demonstrate problem-solving skills"
            ]
        }
        
        return instructions.get(interview_type, instructions["mixed"])
    
    def evaluate_response(self, session_config: Dict, question: Dict, response: str, response_time: int) -> Dict[str, Any]:
        """Comprehensive response evaluation with real-time feedback"""
        
        if not response or len(response.strip()) < 10:
            return self._generate_empty_response_evaluation(question)
        
        cleaned_response = response.strip().lower()
        word_count = len(response.split())
        
        evaluation = {
            'question_id': question['id'],
            'question_type': question['type'],
            'response_length': len(response),
            'word_count': word_count,
            'response_time_seconds': response_time,
            'evaluation_timestamp': datetime.now().isoformat()
        }
        
        # Evaluate different aspects
        evaluation['content_evaluation'] = self._evaluate_content_quality(question, cleaned_response)
        evaluation['communication_evaluation'] = self._evaluate_communication_skills(response)
        evaluation['star_method_evaluation'] = self._evaluate_star_method(question, cleaned_response)
        evaluation['confidence_evaluation'] = self._evaluate_confidence_presence(response)
        evaluation['time_management_evaluation'] = self._evaluate_time_management(question, response_time, word_count)
        
        # Calculate overall scores
        evaluation['overall_score'] = self._calculate_response_score(evaluation)
        evaluation['strengths'] = self._identify_response_strengths(evaluation)
        evaluation['areas_for_improvement'] = self._identify_improvement_areas(evaluation)
        evaluation['specific_feedback'] = self._generate_specific_feedback(question, evaluation)
        evaluation['ml_features'] = self._extract_interview_ml_features(evaluation)
        
        return evaluation
    
    def _evaluate_content_quality(self, question: Dict, response: str) -> Dict[str, Any]:
        """Evaluate the quality and relevance of response content"""
        
        expected_elements = question.get('expected_elements', [])
        elements_covered = []
        
        element_keywords = {
            'background': ['background', 'experience', 'studied', 'worked'],
            'experience': ['experience', 'worked', 'project', 'role', 'position'],
            'skills': ['skills', 'knowledge', 'ability', 'proficient'],
            'goals': ['goal', 'aim', 'objective', 'want', 'plan'],
            'situation': ['situation', 'when', 'time', 'context'],
            'task': ['task', 'needed', 'had to', 'responsible'],
            'action': ['action', 'did', 'took', 'implemented'],
            'result': ['result', 'outcome', 'achieved', 'successful'],
            'weakness': ['weakness', 'struggle', 'challenge'],
            'improvement_plan': ['improve', 'working on', 'plan', 'practice']
        }
        
        for element in expected_elements:
            if element in element_keywords:
                if any(keyword in response for keyword in element_keywords[element]):
                    elements_covered.append(element)
        
        element_coverage = (len(elements_covered) / max(len(expected_elements), 1)) * 100
        
        example_indicators = ['example', 'instance', 'specifically', 'time when']
        has_examples = any(indicator in response for indicator in example_indicators)
        
        content_score = element_coverage * 0.7 + (30 if has_examples else 0) * 0.3
        
        return {
            'expected_elements': expected_elements,
            'elements_covered': elements_covered,
            'element_coverage_percentage': round(element_coverage, 2),
            'has_specific_examples': has_examples,
            'content_quality_score': round(content_score, 2)
        }
    
    def _evaluate_communication_skills(self, response: str) -> Dict[str, Any]:
        """Evaluate communication clarity and structure"""
        
        sentences = response.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        
        structure_indicators = ['first', 'second', 'then', 'next', 'finally', 'furthermore']
        structure_score = min(100, sum(1 for indicator in structure_indicators if indicator.lower() in response.lower()) * 20)
        
        filler_words = ['um', 'uh', 'like', 'you know', 'basically']
        filler_count = sum(response.lower().count(filler) for filler in filler_words)
        
        clarity_score = max(0, 100 - max(0, (avg_sentence_length - 20) * 2) - filler_count * 5)
        communication_score = (structure_score * 0.4 + clarity_score * 0.6)
        
        return {
            'average_sentence_length': round(avg_sentence_length, 2),
            'structure_score': round(structure_score, 2),
            'filler_words_count': filler_count,
            'clarity_score': round(clarity_score, 2),
            'communication_score': round(communication_score, 2)
        }
    
    def _evaluate_star_method(self, question: Dict, response: str) -> Dict[str, Any]:
        """Evaluate use of STAR method for behavioral questions"""
        
        if question.get('type') not in ['problem_solving', 'teamwork', 'leadership']:
            return {'applicable': False, 'star_score': 0, 'components_present': {}}
        
        star_components = {}
        for component, keywords in self.star_method_keywords.items():
            component_found = any(keyword in response for keyword in keywords)
            star_components[component] = component_found
        
        components_present = sum(star_components.values())
        star_score = (components_present / 4) * 100
        
        return {
            'applicable': True,
            'star_score': round(star_score, 2),
            'components_present': star_components,
            'components_count': components_present
        }
    
    def _evaluate_confidence_presence(self, response: str) -> Dict[str, Any]:
        """Evaluate confidence and professional presence"""
        
        confidence_indicators = ['i successfully', 'i achieved', 'i led', 'i managed', 'confident', 'accomplished']
        uncertainty_indicators = ['i think', 'maybe', 'perhaps', 'i guess', 'not sure']
        
        confidence_count = sum(1 for indicator in confidence_indicators if indicator in response.lower())
        uncertainty_count = sum(1 for indicator in uncertainty_indicators if indicator in response.lower())
        
        confidence_score = max(0, min(100, confidence_count * 20 - uncertainty_count * 15 + 50))
        
        return {
            'confidence_indicators_count': confidence_count,
            'uncertainty_indicators_count': uncertainty_count,
            'confidence_score': round(confidence_score, 2)
        }
    
    def _evaluate_time_management(self, question: Dict, response_time: int, word_count: int) -> Dict[str, Any]:
        """Evaluate time management and response appropriateness"""
        
        time_limit = question.get('time_limit', 120)
        expected_word_range = (50, 200)
        
        within_time = response_time <= time_limit
        length_appropriate = expected_word_range[0] <= word_count <= expected_word_range[1]
        
        time_score = (50 if within_time else 25) + (50 if length_appropriate else 25)
        
        return {
            'response_time_seconds': response_time,
            'time_limit_seconds': time_limit,
            'within_time_limit': within_time,
            'word_count': word_count,
            'length_appropriate': length_appropriate,
            'time_management_score': round(time_score, 2)
        }
    
    def _calculate_response_score(self, evaluation: Dict) -> float:
        """Calculate weighted overall response score"""
        
        scores = {
            'content_quality': evaluation.get('content_evaluation', {}).get('content_quality_score', 0),
            'communication_skills': evaluation.get('communication_evaluation', {}).get('communication_score', 0),
            'star_method_usage': evaluation.get('star_method_evaluation', {}).get('star_score', 0),
            'confidence_presence': evaluation.get('confidence_evaluation', {}).get('confidence_score', 0),
            'time_management': evaluation.get('time_management_evaluation', {}).get('time_management_score', 0)
        }
        
        weighted_score = 0
        for criterion, weight_info in self.evaluation_criteria.items():
            weight = weight_info['weight']
            score = scores.get(criterion, 0)
            weighted_score += score * weight
        
        return round(weighted_score, 2)
    
    def _identify_response_strengths(self, evaluation: Dict) -> List[str]:
        """Identify strengths in the response"""
        strengths = []
        
        if evaluation.get('content_evaluation', {}).get('content_quality_score', 0) >= 80:
            strengths.append("Comprehensive and relevant content")
        
        if evaluation.get('content_evaluation', {}).get('has_specific_examples', False):
            strengths.append("Good use of specific examples")
        
        if evaluation.get('communication_evaluation', {}).get('communication_score', 0) >= 80:
            strengths.append("Clear and well-structured communication")
        
        if evaluation.get('star_method_evaluation', {}).get('star_score', 0) >= 75:
            strengths.append("Excellent use of STAR method")
        
        if evaluation.get('confidence_evaluation', {}).get('confidence_score', 0) >= 80:
            strengths.append("Confident and professional delivery")
        
        return strengths if strengths else ["Response provided with genuine effort"]
    
    def _identify_improvement_areas(self, evaluation: Dict) -> List[str]:
        """Identify areas needing improvement"""
        improvements = []
        
        if evaluation.get('content_evaluation', {}).get('element_coverage_percentage', 0) < 60:
            improvements.append("Address more of the key question elements")
        
        if not evaluation.get('content_evaluation', {}).get('has_specific_examples', False):
            improvements.append("Include specific examples to illustrate your points")
        
        if evaluation.get('communication_evaluation', {}).get('filler_words_count', 0) > 3:
            improvements.append("Reduce use of filler words")
        
        star_eval = evaluation.get('star_method_evaluation', {})
        if star_eval.get('applicable', False) and star_eval.get('star_score', 0) < 50:
            improvements.append("Better utilize the STAR method for behavioral questions")
        
        if evaluation.get('time_management_evaluation', {}).get('time_management_score', 0) < 60:
            improvements.append("Work on time management and response length")
        
        return improvements
    
    def _generate_specific_feedback(self, question: Dict, evaluation: Dict) -> List[str]:
        """Generate specific, actionable feedback"""
        feedback = []
        
        if question.get('type') == 'introduction':
            if evaluation.get('content_evaluation', {}).get('element_coverage_percentage', 0) < 75:
                feedback.append("💡 For 'Tell me about yourself', cover: background, experience, skills, and goals")
        
        elif question.get('type') in ['problem_solving', 'teamwork']:
            star_components = evaluation.get('star_method_evaluation', {}).get('components_present', {})
            missing = [comp for comp, present in star_components.items() if not present]
            if missing:
                feedback.append(f"📋 STAR Method: Include {', '.join(missing).title()}")
        
        if evaluation.get('communication_evaluation', {}).get('filler_words_count', 0) > 2:
            feedback.append("🗣️ Minimize filler words for more professional delivery")
        
        if not evaluation.get('content_evaluation', {}).get('has_specific_examples', False):
            feedback.append("🎯 Add specific examples with concrete outcomes")
        
        return feedback
    
    def _generate_empty_response_evaluation(self, question: Dict) -> Dict[str, Any]:
        """Generate evaluation for empty or insufficient response"""
        return {
            'question_id': question['id'],
            'question_type': question['type'],
            'response_length': 0,
            'word_count': 0,
            'overall_score': 0,
            'strengths': [],
            'areas_for_improvement': ['Provide a complete response to the question'],
            'specific_feedback': ['Please provide a response to receive feedback']
        }
    
    def _extract_interview_ml_features(self, evaluation: Dict) -> Dict[str, float]:
        """Extract features for ML model integration"""
        return {
            'interview_overall_score': evaluation.get('overall_score', 0),
            'interview_content_score': evaluation.get('content_evaluation', {}).get('content_quality_score', 0),
            'interview_communication_score': evaluation.get('communication_evaluation', {}).get('communication_score', 0),
            'interview_star_method_score': evaluation.get('star_method_evaluation', {}).get('star_score', 0),
            'interview_confidence_score': evaluation.get('confidence_evaluation', {}).get('confidence_score', 0),
            'interview_time_management_score': evaluation.get('time_management_evaluation', {}).get('time_management_score', 0),
            'interview_response_length': evaluation.get('word_count', 0),
            'interview_response_time': evaluation.get('response_time_seconds', 0)
        }

def main():
    """Test the mock interview engine"""
    print("🎤 Testing Mock Interview Engine")
    print("=" * 50)
    
    engine = MockInterviewEngine()
    
    # Generate interview session
    session = engine.generate_interview_session("behavioral", 15)
    print(f"Generated interview session with {session['total_questions']} questions")
    
    # Test with sample response
    sample_question = session['questions'][0]
    sample_response = """
    I'm a software developer with 3 years of experience in web development. 
    I have a strong background in JavaScript and Python, and I've worked on several 
    full-stack projects. Recently, I completed a challenging e-commerce project where 
    I led a team of 3 developers. We successfully delivered the project on time and 
    it resulted in a 25% increase in online sales. I'm passionate about creating 
    efficient solutions and I'm looking to grow into a senior developer role where 
    I can mentor others and work on more complex systems.
    """
    
    # Evaluate response
    evaluation = engine.evaluate_response(session, sample_question, sample_response, 90)
    
    print(f"\nEvaluation Results:")
    print(f"Overall Score: {evaluation['overall_score']:.1f}/100")
    print(f"Content Quality: {evaluation['content_evaluation']['content_quality_score']:.1f}/100")
    print(f"Communication: {evaluation['communication_evaluation']['communication_score']:.1f}/100")
    
    print(f"\nStrengths:")
    for strength in evaluation['strengths']:
        print(f"  • {strength}")
    
    print(f"\nAreas for Improvement:")
    for improvement in evaluation['areas_for_improvement']:
        print(f"  • {improvement}")
    
    print(f"\nSpecific Feedback:")
    for feedback in evaluation['specific_feedback']:
        print(f"  • {feedback}")
    
    print("\n✅ Mock Interview Engine test completed!")

if __name__ == "__main__":
    main()