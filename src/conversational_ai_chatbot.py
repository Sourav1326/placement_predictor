"""
💬 CONVERSATIONAL AI CHATBOT
Context-aware intelligent assistant for placement prediction system
"""

import re
import json
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
import difflib

class ConversationalAIChatbot:
    """
    Intelligent chatbot with context awareness and proactive assistance
    """
    
    def __init__(self):
        self.conversation_history = {}  # user_id -> conversation history
        self.user_context = {}  # user_id -> current context
        self.intent_patterns = self._load_intent_patterns()
        self.responses = self._load_responses()
        self.proactive_triggers = self._load_proactive_triggers()
        self.quick_actions = self._load_quick_actions()
    
    def process_message(self, user_id: int, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process user message and generate intelligent response"""
        
        # Update user context
        if context:
            self.user_context[user_id] = {**self.user_context.get(user_id, {}), **context}
        
        # Initialize conversation history
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        # Add user message to history
        self.conversation_history[user_id].append({
            'sender': 'user',
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Detect intent
        intent = self._detect_intent(message)
        
        # Generate context-aware response
        response = self._generate_response(user_id, intent, message)
        
        # Add bot response to history
        self.conversation_history[user_id].append({
            'sender': 'bot',
            'message': response['message'],
            'intent': intent,
            'timestamp': datetime.now().isoformat()
        })
        
        return response
    
    def generate_proactive_message(self, user_id: int, trigger_event: str, 
                                 event_data: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Generate proactive messages based on user actions"""
        
        context = self.user_context.get(user_id, {})
        
        # Check if we should send a proactive message
        trigger_config = self.proactive_triggers.get(trigger_event)
        if not trigger_config:
            return None
        
        # Generate contextual proactive message
        message_template = random.choice(trigger_config['messages'])
        
        # Personalize message based on context and event data
        personalized_message = self._personalize_message(
            message_template, context, event_data
        )
        
        # Add to conversation history
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        response = {
            'message': personalized_message,
            'type': 'proactive',
            'trigger': trigger_event,
            'quick_replies': trigger_config.get('quick_replies', []),
            'actions': trigger_config.get('actions', [])
        }
        
        self.conversation_history[user_id].append({
            'sender': 'bot',
            'message': personalized_message,
            'type': 'proactive',
            'timestamp': datetime.now().isoformat()
        })
        
        return response
    
    def get_suggested_actions(self, user_id: int) -> List[Dict[str, Any]]:
        """Get personalized action suggestions based on user context"""
        context = self.user_context.get(user_id, {})
        suggestions = []
        
        # Assessment suggestions
        if not context.get('completed_aptitude_test'):
            suggestions.append({
                'title': '🧠 Take Aptitude Test',
                'description': 'Assess your logical reasoning and problem-solving skills',
                'action': 'start_aptitude_test',
                'priority': 'high'
            })
        
        if not context.get('completed_skill_verification'):
            suggestions.append({
                'title': '✅ Verify Your Skills',
                'description': 'Get verified badges for your technical skills',
                'action': 'start_skill_verification',
                'priority': 'high'
            })
        
        if not context.get('resume_uploaded'):
            suggestions.append({
                'title': '📄 Upload Resume',
                'description': 'Get ATS compatibility check and autofill your profile',
                'action': 'upload_resume',
                'priority': 'medium'
            })
        
        # Improvement suggestions based on scores
        if context.get('last_prediction_score', 0) < 0.7:
            suggestions.append({
                'title': '📈 Improve Placement Chances',
                'description': 'Get personalized recommendations to boost your score',
                'action': 'view_recommendations',
                'priority': 'high'
            })
        
        return suggestions
    
    def _detect_intent(self, message: str) -> str:
        """Detect user intent from message"""
        message_lower = message.lower().strip()
        
        # Direct keyword matching
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    return intent
        
        # Fuzzy matching for common intents
        common_intents = ['take_test', 'help', 'prediction', 'skills', 'resume']
        for intent in common_intents:
            if difflib.SequenceMatcher(None, intent.replace('_', ' '), message_lower).ratio() > 0.6:
                return intent
        
        return 'unknown'
    
    def _generate_response(self, user_id: int, intent: str, message: str) -> Dict[str, Any]:
        """Generate context-aware response based on intent"""
        context = self.user_context.get(user_id, {})
        
        # Get base response for intent
        base_responses = self.responses.get(intent, self.responses['unknown'])
        response_template = random.choice(base_responses['messages'])
        
        # Personalize response
        personalized_message = self._personalize_message(response_template, context)
        
        # Get quick replies and actions
        quick_replies = base_responses.get('quick_replies', [])
        actions = base_responses.get('actions', [])
        
        # Add context-specific quick replies
        if intent == 'take_test':
            if not context.get('completed_aptitude_test'):
                quick_replies.append('Aptitude Test')
            if not context.get('completed_skill_verification'):
                quick_replies.append('Skill Verification')
            if not context.get('completed_communication_test'):
                quick_replies.append('Communication Test')
        
        return {
            'message': personalized_message,
            'type': 'response',
            'intent': intent,
            'quick_replies': quick_replies,
            'actions': actions,
            'suggestions': self.get_suggested_actions(user_id)
        }
    
    def _personalize_message(self, template: str, context: Dict[str, Any], 
                           event_data: Dict[str, Any] = None) -> str:
        """Personalize message template with user context"""
        
        # Replace context variables
        message = template
        
        if '{name}' in message:
            name = context.get('name', 'there')
            message = message.replace('{name}', name)
        
        if '{score}' in message and event_data:
            score = event_data.get('score', context.get('last_prediction_score', 0))
            if isinstance(score, float):
                score = f"{score*100:.1f}%"
            message = message.replace('{score}', str(score))
        
        if '{missing_skills}' in message and event_data:
            skills = event_data.get('missing_skills', [])
            if skills:
                skills_text = ', '.join(skills[:3])
                message = message.replace('{missing_skills}', skills_text)
        
        return message
    
    def _load_intent_patterns(self) -> Dict[str, List[str]]:
        """Load intent detection patterns"""
        return {
            'greeting': [
                r'\b(hi|hello|hey|good morning|good afternoon)\b',
                r'\bwhat\'s up\b',
                r'\bhow are you\b'
            ],
            'help': [
                r'\b(help|assist|support)\b',
                r'\bhow do i\b',
                r'\bwhat can you do\b',
                r'\bi need help\b'
            ],
            'take_test': [
                r'\b(test|assessment|quiz|exam)\b',
                r'\btake.*test\b',
                r'\bstart.*assessment\b',
                r'\bskill.*verification\b'
            ],
            'prediction': [
                r'\b(prediction|predict|chance|probability)\b',
                r'\bplacement.*score\b',
                r'\bhow likely\b',
                r'\bwhat are my chances\b'
            ],
            'skills': [
                r'\b(skill|technology|programming)\b',
                r'\bwhat skills\b',
                r'\blearn.*skill\b',
                r'\bimprove.*skill\b'
            ],
            'resume': [
                r'\b(resume|cv|curriculum vitae)\b',
                r'\bats.*check\b',
                r'\bupload.*resume\b',
                r'\bresume.*score\b'
            ],
            'courses': [
                r'\b(course|learning|training|education)\b',
                r'\brecommend.*course\b',
                r'\bwhat to learn\b'
            ],
            'companies': [
                r'\b(company|job|placement|interview)\b',
                r'\bwhich companies\b',
                r'\bjob opportunities\b'
            ]
        }
    
    def _load_responses(self) -> Dict[str, Dict[str, Any]]:
        """Load response templates for each intent"""
        return {
            'greeting': {
                'messages': [
                    "Hi {name}! 👋 I'm your placement assistant. How can I help you today?",
                    "Hello! Ready to boost your placement chances? What would you like to do?",
                    "Hey there! I'm here to help you with assessments, predictions, and career guidance!"
                ],
                'quick_replies': ['Take Assessment', 'Check Prediction', 'Upload Resume', 'Get Help'],
                'actions': []
            },
            'help': {
                'messages': [
                    "I can help you with:\n• Taking skill assessments\n• Checking placement predictions\n• Analyzing your resume\n• Finding courses and jobs\n• Getting personalized recommendations\n\nWhat interests you most?",
                    "Here's what I can do for you:\n🧠 Aptitude & skill tests\n📊 Placement probability analysis\n📄 Resume ATS checking\n📚 Course recommendations\n🔍 Job matching\n\nJust ask!"
                ],
                'quick_replies': ['Assessments', 'Predictions', 'Resume Check', 'Courses'],
                'actions': ['show_features']
            },
            'take_test': {
                'messages': [
                    "Great choice! Taking assessments will significantly boost your placement prediction accuracy. Which type of assessment would you like to start with?",
                    "Excellent! Verified skills can increase your placement probability by up to 40%. What would you like to assess first?"
                ],
                'quick_replies': ['Aptitude Test', 'Skill Verification', 'Communication Test', 'Mock Interview'],
                'actions': ['navigate_to_assessments']
            },
            'prediction': {
                'messages': [
                    "I can calculate your placement probability based on your profile and verified skills. Your current prediction score is {score}. Want to see detailed analysis?",
                    "Your placement chances depend on your skills, education, and performance in assessments. Let me analyze your profile!"
                ],
                'quick_replies': ['Show Prediction', 'Improve Score', 'Take Assessments'],
                'actions': ['show_prediction']
            },
            'skills': {
                'messages': [
                    "Skills are crucial for placement! I can help you:\n• Verify your existing skills\n• Identify skill gaps\n• Recommend learning paths\n• Find relevant courses\n\nWhat specifically would you like to work on?",
                    "Let's enhance your skillset! Based on market demand, these skills are highly valued: Python, SQL, React, AWS. Want to get verified in any of these?"
                ],
                'quick_replies': ['Verify Skills', 'Learn New Skills', 'Skill Gap Analysis'],
                'actions': ['show_skills_dashboard']
            },
            'resume': {
                'messages': [
                    "Resume optimization is key for ATS systems! I can:\n• Check ATS compatibility\n• Score your resume\n• Auto-fill your profile\n• Suggest improvements\n\nHave you uploaded your resume yet?",
                    "Most resumes fail ATS screening! Let me help you create an ATS-friendly resume that gets noticed by recruiters."
                ],
                'quick_replies': ['Upload Resume', 'ATS Check', 'Resume Tips'],
                'actions': ['navigate_to_resume']
            },
            'courses': {
                'messages': [
                    "Learning never stops! I can recommend personalized courses based on:\n• Your current skills\n• Target companies\n• Market demand\n• Skill gaps\n\nWhat's your learning goal?",
                    "Great question! Based on your profile, I can suggest courses that will maximize your placement chances. What area interests you most?"
                ],
                'quick_replies': ['Technical Skills', 'Soft Skills', 'Certifications', 'Company-Specific'],
                'actions': ['show_course_recommendations']
            },
            'companies': {
                'messages': [
                    "I can help you target the right companies! Based on your skills and profile, I'll suggest:\n• Company tiers you're ready for\n• Live job openings\n• Required skills for dream companies\n• Interview preparation\n\nWhat's your target company type?",
                    "Company targeting is smart strategy! Let me analyze which companies are the best fit for your current profile and verified skills."
                ],
                'quick_replies': ['Tier 1 (Google, Amazon)', 'Tier 2 (TCS, Infosys)', 'Startups', 'All Options'],
                'actions': ['show_company_predictions']
            },
            'unknown': {
                'messages': [
                    "I'm not sure I understood that. I can help you with assessments, predictions, resume checking, courses, and job matching. What would you like to explore?",
                    "Could you rephrase that? I'm here to help with your placement journey - from skill verification to job matching!"
                ],
                'quick_replies': ['Take Assessment', 'Check Prediction', 'Upload Resume', 'Get Help'],
                'actions': []
            }
        }
    
    def _load_proactive_triggers(self) -> Dict[str, Dict[str, Any]]:
        """Load proactive message triggers and templates"""
        return {
            'low_ats_score': {
                'messages': [
                    "I noticed your resume might not be ATS-friendly (score: {score}). I have proven templates that can help improve your score. Would you like to see them?",
                    "Your ATS score of {score} could be improved! Let me show you exactly what recruiters' systems are looking for."
                ],
                'quick_replies': ['Show ATS Tips', 'Get Template', 'Manual Review'],
                'actions': ['show_ats_recommendations']
            },
            'failed_assessment': {
                'messages': [
                    "Don't worry about the assessment result! I can help you identify exactly what to study and recommend personalized learning resources. Ready to improve?",
                    "Every expert was once a beginner! Let me create a custom learning plan based on your assessment performance."
                ],
                'quick_replies': ['Study Plan', 'Practice More', 'Different Assessment'],
                'actions': ['create_study_plan']
            },
            'low_prediction_score': {
                'messages': [
                    "Your placement probability is {score}. The good news? I know exactly how to improve it! Top recommendations: verify your skills and complete assessments.",
                    "With your current profile, you're at {score} placement probability. Let's get you to 90%+ with targeted improvements!"
                ],
                'quick_replies': ['Verify Skills', 'Take Assessments', 'Improve Profile'],
                'actions': ['show_improvement_plan']
            },
            'skill_gap_identified': {
                'messages': [
                    "I found some skill gaps for your target companies: {missing_skills}. Want me to find the best courses to fill these gaps?",
                    "To reach your target companies, consider learning: {missing_skills}. I can recommend the most effective learning path!"
                ],
                'quick_replies': ['Show Courses', 'Skill Priorities', 'Alternative Paths'],
                'actions': ['recommend_courses']
            },
            'assessment_completed': {
                'messages': [
                    "Congratulations on completing the assessment! 🎉 Your performance has been added to your profile. Want to see how it affects your placement prediction?",
                    "Great job! Your verified skills now carry more weight in predictions. Ready to tackle another assessment or see your updated score?"
                ],
                'quick_replies': ['View Updated Score', 'Take Another Test', 'Share Achievement'],
                'actions': ['update_prediction']
            }
        }
    
    def _load_quick_actions(self) -> Dict[str, Dict[str, Any]]:
        """Load quick action configurations"""
        return {
            'start_aptitude_test': {
                'url': '/comprehensive-assessment',
                'description': 'Begin comprehensive aptitude assessment'
            },
            'start_skill_verification': {
                'url': '/skill-verification',
                'description': 'Verify your technical skills'
            },
            'upload_resume': {
                'url': '/resume-scorer',
                'description': 'Upload and analyze your resume'
            },
            'view_prediction': {
                'url': '/placement-prediction',
                'description': 'Check your placement probability'
            },
            'browse_courses': {
                'url': '/course-recommendations',
                'description': 'Find personalized course recommendations'
            }
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize chatbot
    chatbot = ConversationalAIChatbot()
    
    # Test conversations
    test_messages = [
        "Hi there!",
        "I want to take a test",
        "How can I improve my placement chances?",
        "Help me with my resume",
        "What skills should I learn?"
    ]
    
    print("💬 Conversational AI Chatbot Test:")
    
    user_id = 1
    for message in test_messages:
        print(f"\nUser: {message}")
        response = chatbot.process_message(user_id, message)
        print(f"Bot: {response['message']}")
        if response.get('quick_replies'):
            print(f"Quick Replies: {response['quick_replies']}")
    
    # Test proactive message
    print(f"\n📢 Proactive Message Test:")
    proactive = chatbot.generate_proactive_message(
        user_id, 
        'low_ats_score', 
        {'score': '45%'}
    )
    if proactive:
        print(f"Proactive: {proactive['message']}")
    
    print("\n✅ Conversational AI Chatbot ready for integration!")