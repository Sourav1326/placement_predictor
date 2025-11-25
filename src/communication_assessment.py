"""
Automated Written Communication Test with NLP Scoring
Advanced Natural Language Processing for communication assessment
"""

import re
import nltk
import string
from typing import Dict, List, Any, Tuple
from datetime import datetime
import numpy as np

try:
    from textstat import flesch_kincaid_grade, flesch_reading_ease, syllable_count
    TEXTSTAT_AVAILABLE = True
except ImportError:
    TEXTSTAT_AVAILABLE = False
    print("⚠️ textstat not available. Install with: pip install textstat")

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    print("⚠️ TextBlob not available. Install with: pip install textblob")

class CommunicationAssessmentEngine:
    """
    Advanced NLP-based communication assessment engine
    """
    
    def __init__(self):
        self.writing_prompts = self._load_writing_prompts()
        self.professional_vocabulary = self._load_professional_vocabulary()
        self.common_errors = self._load_common_errors()
        self._ensure_nltk_data()
        
    def _ensure_nltk_data(self):
        """Ensure required NLTK data is downloaded"""
        try:
            import nltk
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("Downloading NLTK data...")
            try:
                nltk.download('punkt', quiet=True)
                nltk.download('averaged_perceptron_tagger', quiet=True)
                nltk.download('vader_lexicon', quiet=True)
            except:
                print("⚠️ Could not download NLTK data. Some features may be limited.")
    
    def _load_writing_prompts(self) -> Dict[str, Dict]:
        """Load various writing prompts for assessment"""
        return {
            "email_project_extension": {
                "title": "Project Extension Request",
                "prompt": "Write a professional email to your manager requesting a 2-week extension for your current project due to unexpected technical challenges. Explain the situation and propose a solution.",
                "type": "professional_email",
                "expected_elements": ["greeting", "purpose", "explanation", "solution", "timeline", "closing"],
                "word_limit": 200,
                "time_limit": 900  # 15 minutes
            },
            "client_complaint_response": {
                "title": "Client Complaint Response", 
                "prompt": "A client has complained about delayed delivery of their software project. Write a professional response acknowledging the issue, apologizing, and outlining steps to resolve the problem.",
                "type": "professional_email",
                "expected_elements": ["acknowledgment", "apology", "explanation", "resolution_steps", "prevention_measures"],
                "word_limit": 250,
                "time_limit": 900
            },
            "team_collaboration_proposal": {
                "title": "Team Collaboration Proposal",
                "prompt": "Your team is working remotely and facing communication issues. Write a proposal to your team lead suggesting improvements to enhance collaboration and productivity.",
                "type": "proposal",
                "expected_elements": ["problem_identification", "proposed_solutions", "benefits", "implementation_plan"],
                "word_limit": 300,
                "time_limit": 1200  # 20 minutes
            },
            "technical_explanation": {
                "title": "Technical Concept Explanation",
                "prompt": "Explain the concept of 'Machine Learning' to a non-technical stakeholder in your organization who needs to understand its business applications.",
                "type": "explanation",
                "expected_elements": ["definition", "simplified_explanation", "business_applications", "examples"],
                "word_limit": 250,
                "time_limit": 900
            },
            "meeting_summary": {
                "title": "Meeting Summary Report",
                "prompt": "Write a summary of a project status meeting including: 3 completed tasks, 2 ongoing challenges, 2 upcoming milestones, and 1 resource requirement. Make it concise and actionable.",
                "type": "report",
                "expected_elements": ["completed_tasks", "challenges", "milestones", "resources", "action_items"],
                "word_limit": 200,
                "time_limit": 900
            }
        }
    
    def _load_professional_vocabulary(self) -> Dict[str, List[str]]:
        """Load professional vocabulary for different contexts"""
        return {
            "business_formal": [
                "regarding", "furthermore", "consequently", "nevertheless", "therefore",
                "implementation", "collaboration", "optimization", "enhancement", "deliverable",
                "stakeholder", "milestone", "objective", "strategy", "initiative"
            ],
            "technical": [
                "algorithm", "architecture", "implementation", "framework", "optimization",
                "scalability", "performance", "debugging", "integration", "deployment",
                "methodology", "specification", "documentation", "testing", "validation"
            ],
            "professional_courtesy": [
                "appreciate", "grateful", "pleased", "honored", "respect",
                "consider", "understand", "acknowledge", "assist", "support",
                "professional", "courteous", "prompt", "efficient", "quality"
            ]
        }
    
    def _load_common_errors(self) -> Dict[str, List[str]]:
        """Load patterns of common writing errors"""
        return {
            "informal_contractions": [
                "can't", "won't", "don't", "isn't", "aren't", "wasn't", "weren't",
                "hasn't", "haven't", "hadn't", "shouldn't", "wouldn't", "couldn't"
            ],
            "informal_phrases": [
                "gonna", "wanna", "kinda", "sorta", "yeah", "ok", "btw", "fyi",
                "asap", "etc.", "i.e.", "e.g."  # These should be written out in formal writing
            ],
            "weak_words": [
                "really", "very", "quite", "pretty", "somewhat", "rather",
                "kind of", "sort of", "a bit", "a little"
            ]
        }
    
    def generate_communication_test(self, test_type: str = "mixed", difficulty: str = "medium") -> Dict[str, Any]:
        """Generate a communication assessment test"""
        
        if test_type == "mixed":
            # Select diverse prompts
            selected_prompts = list(self.writing_prompts.keys())[:3]
        else:
            # Filter by type
            selected_prompts = [k for k, v in self.writing_prompts.items() 
                             if v.get('type') == test_type][:3]
        
        if not selected_prompts:
            selected_prompts = list(self.writing_prompts.keys())[:3]
        
        test_config = {
            'test_id': f"comm_test_{int(datetime.now().timestamp())}",
            'test_type': test_type,
            'difficulty': difficulty,
            'prompts': [self.writing_prompts[prompt_key] for prompt_key in selected_prompts],
            'total_prompts': len(selected_prompts),
            'total_time': sum(self.writing_prompts[p]['time_limit'] for p in selected_prompts),
            'instructions': self._get_communication_test_instructions(),
            'evaluation_criteria': {
                'grammar_spelling': 25,  # 25% weight
                'clarity_readability': 25,  # 25% weight
                'professionalism': 20,  # 20% weight
                'content_structure': 20,  # 20% weight
                'vocabulary_usage': 10   # 10% weight
            }
        }
        
        return test_config
    
    def _get_communication_test_instructions(self) -> List[str]:
        """Get instructions for communication test"""
        return [
            "This test evaluates your written communication skills in professional contexts.",
            "Write clear, concise, and professional responses to each prompt.",
            "Pay attention to grammar, spelling, tone, and structure.",
            "Use appropriate business vocabulary and maintain professional etiquette.",
            "Aim for clarity and avoid overly complex sentences.",
            "Proofread your responses before submitting.",
            "Each prompt has a recommended word limit - stay within reasonable bounds."
        ]
    
    def evaluate_written_response(self, prompt_config: Dict, user_response: str, 
                                time_taken: int) -> Dict[str, Any]:
        """
        Comprehensive evaluation of written response using NLP techniques
        """
        
        if not user_response or len(user_response.strip()) < 10:
            return self._generate_empty_response_result(prompt_config)
        
        # Clean the response
        cleaned_response = user_response.strip()
        
        # Initialize evaluation results
        evaluation = {
            'prompt_id': prompt_config.get('title', 'Unknown'),
            'response_length': len(cleaned_response),
            'word_count': len(cleaned_response.split()),
            'time_taken': time_taken,
            'timestamp': datetime.now().isoformat()
        }
        
        # 1. Grammar and Spelling Analysis
        grammar_spelling = self._analyze_grammar_spelling(cleaned_response)
        evaluation['grammar_spelling'] = grammar_spelling
        
        # 2. Clarity and Readability Analysis
        clarity_readability = self._analyze_clarity_readability(cleaned_response)
        evaluation['clarity_readability'] = clarity_readability
        
        # 3. Professionalism Analysis
        professionalism = self._analyze_professionalism(cleaned_response, prompt_config)
        evaluation['professionalism'] = professionalism
        
        # 4. Content Structure Analysis
        content_structure = self._analyze_content_structure(cleaned_response, prompt_config)
        evaluation['content_structure'] = content_structure
        
        # 5. Vocabulary Usage Analysis
        vocabulary_usage = self._analyze_vocabulary_usage(cleaned_response)
        evaluation['vocabulary_usage'] = vocabulary_usage
        
        # Calculate overall scores
        evaluation['overall_score'] = self._calculate_overall_score(evaluation)
        evaluation['grade'] = self._assign_grade(evaluation['overall_score'])
        evaluation['detailed_feedback'] = self._generate_detailed_feedback(evaluation)
        evaluation['improvement_suggestions'] = self._generate_improvement_suggestions(evaluation)
        
        # Extract ML features
        evaluation['ml_features'] = self._extract_communication_ml_features(evaluation)
        
        return evaluation
    
    def _analyze_grammar_spelling(self, text: str) -> Dict[str, Any]:
        """Analyze grammar and spelling using various techniques"""
        analysis = {
            'score': 85,  # Default score, will be adjusted
            'errors_found': [],
            'error_count': 0,
            'error_types': {}
        }
        
        # Basic spell checking using common patterns
        words = text.split()
        potential_errors = []
        
        # Check for common contractions in formal writing
        contractions_found = []
        for word in words:
            word_lower = word.lower().strip('.,!?";:')
            if word_lower in self.common_errors['informal_contractions']:
                contractions_found.append(word)
        
        if contractions_found:
            analysis['errors_found'].append({
                'type': 'informal_contractions',
                'description': f"Avoid contractions in formal writing: {', '.join(set(contractions_found))}",
                'severity': 'medium'
            })
        
        # Check for informal phrases
        text_lower = text.lower()
        informal_phrases_found = []
        for phrase in self.common_errors['informal_phrases']:
            if phrase in text_lower:
                informal_phrases_found.append(phrase)
        
        if informal_phrases_found:
            analysis['errors_found'].append({
                'type': 'informal_language',
                'description': f"Avoid informal expressions: {', '.join(set(informal_phrases_found))}",
                'severity': 'medium'
            })
        
        # Check for sentence structure issues
        sentences = text.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 200:  # Very long sentences
                analysis['errors_found'].append({
                    'type': 'sentence_length',
                    'description': "Consider breaking very long sentences for better readability",
                    'severity': 'low'
                })
                break
        
        # Calculate error count and adjust score
        total_errors = len(analysis['errors_found'])
        analysis['error_count'] = total_errors
        
        # Deduct points based on errors
        if total_errors == 0:
            analysis['score'] = 95
        elif total_errors <= 2:
            analysis['score'] = 85 - (total_errors * 5)
        else:
            analysis['score'] = max(60, 85 - (total_errors * 8))
        
        return analysis
    
    def _analyze_clarity_readability(self, text: str) -> Dict[str, Any]:
        """Analyze text clarity and readability"""
        analysis = {
            'score': 75,
            'readability_metrics': {},
            'clarity_issues': []
        }
        
        # Basic readability calculations (simplified)
        sentences = len([s for s in text.split('.') if s.strip()])
        words = len(text.split())
        avg_words_per_sentence = words / max(1, sentences)
        
        # Simplified readability score
        if avg_words_per_sentence <= 15:
            readability_score = 90
        elif avg_words_per_sentence <= 20:
            readability_score = 80
        elif avg_words_per_sentence <= 25:
            readability_score = 70
        else:
            readability_score = 60
        
        analysis['readability_metrics'] = {
            'avg_words_per_sentence': round(avg_words_per_sentence, 2),
            'total_sentences': sentences,
            'total_words': words,
            'readability_score': readability_score
        }
        
        # Advanced readability with textstat (if available)
        if TEXTSTAT_AVAILABLE:
            try:
                analysis['readability_metrics'].update({
                    'flesch_kincaid_grade': flesch_kincaid_grade(text),
                    'flesch_reading_ease': flesch_reading_ease(text)
                })
            except:
                pass
        
        # Check for clarity issues
        if avg_words_per_sentence > 25:
            analysis['clarity_issues'].append("Sentences are too long - aim for 15-20 words per sentence")
        
        # Check for repetitive words
        word_freq = {}
        words_lower = [w.lower().strip('.,!?";:') for w in text.split()]
        for word in words_lower:
            if len(word) > 4:  # Only check meaningful words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        repetitive_words = [word for word, count in word_freq.items() if count > 3]
        if repetitive_words:
            analysis['clarity_issues'].append(f"Avoid repetitive use of words: {', '.join(repetitive_words[:3])}")
        
        # Calculate final clarity score
        penalty = len(analysis['clarity_issues']) * 10
        analysis['score'] = max(50, readability_score - penalty)
        
        return analysis
    
    def _analyze_professionalism(self, text: str, prompt_config: Dict) -> Dict[str, Any]:
        """Analyze professional tone and language"""
        analysis = {
            'score': 75,
            'professional_elements': [],
            'unprofessional_elements': [],
            'tone_analysis': {}
        }
        
        text_lower = text.lower()
        
        # Check for professional vocabulary usage
        professional_words_found = 0
        for category, words in self.professional_vocabulary.items():
            for word in words:
                if word in text_lower:
                    professional_words_found += 1
                    analysis['professional_elements'].append(f"Good use of professional term: '{word}'")
        
        # Check for unprofessional elements
        weak_words_found = []
        for weak_word in self.common_errors['weak_words']:
            if weak_word in text_lower:
                weak_words_found.append(weak_word)
        
        if weak_words_found:
            analysis['unprofessional_elements'].append(f"Avoid weak qualifiers: {', '.join(set(weak_words_found))}")
        
        # Sentiment analysis (simplified)
        if TEXTBLOB_AVAILABLE:
            try:
                blob = TextBlob(text)
                sentiment = blob.sentiment
                analysis['tone_analysis'] = {
                    'polarity': round(sentiment.polarity, 3),
                    'subjectivity': round(sentiment.subjectivity, 3),
                    'tone': 'positive' if sentiment.polarity > 0.1 else 'negative' if sentiment.polarity < -0.1 else 'neutral'
                }
                
                if sentiment.polarity < -0.3:
                    analysis['unprofessional_elements'].append("Tone appears overly negative - maintain professional positivity")
            except:
                pass
        
        # Check expected elements for prompt type
        expected_elements = prompt_config.get('expected_elements', [])
        elements_found = 0
        
        for element in expected_elements:
            element_keywords = {
                'greeting': ['dear', 'hello', 'hi'],
                'closing': ['regards', 'sincerely', 'best', 'thank you'],
                'apology': ['sorry', 'apologize', 'regret'],
                'explanation': ['because', 'due to', 'reason'],
                'solution': ['suggest', 'propose', 'recommend', 'plan']
            }
            
            if element in element_keywords:
                if any(keyword in text_lower for keyword in element_keywords[element]):
                    elements_found += 1
                    analysis['professional_elements'].append(f"Included expected element: {element}")
        
        # Calculate professionalism score
        base_score = 70
        professional_bonus = min(20, professional_words_found * 2)
        elements_bonus = min(15, elements_found * 3)
        unprofessional_penalty = len(analysis['unprofessional_elements']) * 10
        
        analysis['score'] = max(40, base_score + professional_bonus + elements_bonus - unprofessional_penalty)
        
        return analysis
    
    def _analyze_content_structure(self, text: str, prompt_config: Dict) -> Dict[str, Any]:
        """Analyze content organization and structure"""
        analysis = {
            'score': 75,
            'structure_elements': [],
            'structure_issues': []
        }
        
        # Check word count appropriateness
        word_count = len(text.split())
        word_limit = prompt_config.get('word_limit', 200)
        
        if word_count < word_limit * 0.5:
            analysis['structure_issues'].append("Response is too brief - provide more detail")
        elif word_count > word_limit * 1.5:
            analysis['structure_issues'].append("Response is too lengthy - be more concise")
        else:
            analysis['structure_elements'].append("Appropriate response length")
        
        # Check for paragraph structure
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        if len(paragraphs) > 1:
            analysis['structure_elements'].append("Good use of paragraphs for organization")
        elif word_count > 100:
            analysis['structure_issues'].append("Consider using paragraphs to organize longer responses")
        
        # Check for logical flow indicators
        flow_indicators = ['first', 'second', 'then', 'next', 'finally', 'in conclusion', 'furthermore', 'however', 'therefore']
        indicators_found = [indicator for indicator in flow_indicators if indicator in text.lower()]
        
        if indicators_found:
            analysis['structure_elements'].append("Good use of transitional phrases for flow")
        
        # Calculate structure score
        base_score = 70
        structure_bonus = len(analysis['structure_elements']) * 8
        structure_penalty = len(analysis['structure_issues']) * 15
        
        analysis['score'] = max(40, base_score + structure_bonus - structure_penalty)
        
        return analysis
    
    def _analyze_vocabulary_usage(self, text: str) -> Dict[str, Any]:
        """Analyze vocabulary richness and usage"""
        analysis = {
            'score': 75,
            'vocabulary_richness': {},
            'vocabulary_feedback': []
        }
        
        words = [w.lower().strip('.,!?";:') for w in text.split() if len(w) > 3]
        unique_words = set(words)
        
        # Calculate vocabulary metrics
        vocabulary_richness = len(unique_words) / max(1, len(words))
        
        analysis['vocabulary_richness'] = {
            'total_words': len(words),
            'unique_words': len(unique_words),
            'richness_ratio': round(vocabulary_richness, 3)
        }
        
        # Provide feedback based on vocabulary richness
        if vocabulary_richness > 0.8:
            analysis['vocabulary_feedback'].append("Excellent vocabulary variety")
            analysis['score'] = 90
        elif vocabulary_richness > 0.6:
            analysis['vocabulary_feedback'].append("Good vocabulary usage")
            analysis['score'] = 80
        elif vocabulary_richness > 0.4:
            analysis['vocabulary_feedback'].append("Adequate vocabulary - try using more varied words")
            analysis['score'] = 70
        else:
            analysis['vocabulary_feedback'].append("Limited vocabulary variety - expand word choice")
            analysis['score'] = 60
        
        return analysis
    
    def _calculate_overall_score(self, evaluation: Dict) -> float:
        """Calculate weighted overall score"""
        weights = {
            'grammar_spelling': 0.25,
            'clarity_readability': 0.25,
            'professionalism': 0.20,
            'content_structure': 0.20,
            'vocabulary_usage': 0.10
        }
        
        total_score = 0
        for component, weight in weights.items():
            if component in evaluation:
                total_score += evaluation[component]['score'] * weight
        
        return round(total_score, 2)
    
    def _assign_grade(self, score: float) -> str:
        """Assign letter grade based on score"""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    def _generate_detailed_feedback(self, evaluation: Dict) -> List[str]:
        """Generate comprehensive feedback"""
        feedback = []
        
        # Overall performance
        score = evaluation['overall_score']
        if score >= 85:
            feedback.append("🌟 Excellent communication skills demonstrated!")
        elif score >= 75:
            feedback.append("👍 Good communication with room for minor improvements")
        elif score >= 65:
            feedback.append("📝 Adequate communication skills, focus on key areas for improvement")
        else:
            feedback.append("📚 Communication skills need significant development")
        
        # Component-specific feedback
        if evaluation['grammar_spelling']['score'] < 70:
            feedback.append("📖 Focus on grammar and spelling - consider proofreading tools")
        
        if evaluation['clarity_readability']['score'] < 70:
            feedback.append("🔍 Work on clarity - use shorter sentences and simpler language")
        
        if evaluation['professionalism']['score'] < 70:
            feedback.append("💼 Enhance professional tone and vocabulary")
        
        if evaluation['content_structure']['score'] < 70:
            feedback.append("🏗️ Improve organization and structure of your writing")
        
        return feedback
    
    def _generate_improvement_suggestions(self, evaluation: Dict) -> List[Dict[str, str]]:
        """Generate specific improvement suggestions"""
        suggestions = []
        
        # Grammar and spelling suggestions
        if evaluation['grammar_spelling']['score'] < 80:
            suggestions.append({
                'area': 'Grammar & Spelling',
                'suggestion': 'Use grammar checking tools like Grammarly or practice with grammar exercises',
                'priority': 'high' if evaluation['grammar_spelling']['score'] < 60 else 'medium'
            })
        
        # Clarity suggestions
        if evaluation['clarity_readability']['score'] < 80:
            suggestions.append({
                'area': 'Clarity & Readability',
                'suggestion': 'Practice writing shorter sentences and use active voice. Read your writing aloud.',
                'priority': 'high' if evaluation['clarity_readability']['score'] < 60 else 'medium'
            })
        
        # Professional tone suggestions
        if evaluation['professionalism']['score'] < 80:
            suggestions.append({
                'area': 'Professional Communication',
                'suggestion': 'Study business email templates and practice professional vocabulary',
                'priority': 'high'
            })
        
        return suggestions
    
    def _extract_communication_ml_features(self, evaluation: Dict) -> Dict[str, float]:
        """Extract features for ML model integration"""
        return {
            'communication_overall_score': evaluation['overall_score'],
            'communication_grammar_score': evaluation['grammar_spelling']['score'],
            'communication_clarity_score': evaluation['clarity_readability']['score'],
            'communication_professionalism_score': evaluation['professionalism']['score'],
            'communication_structure_score': evaluation['content_structure']['score'],
            'communication_vocabulary_score': evaluation['vocabulary_usage']['score'],
            'communication_word_count': evaluation['word_count'],
            'communication_response_time': evaluation['time_taken'],
            'communication_vocabulary_richness': evaluation['vocabulary_usage']['vocabulary_richness']['richness_ratio']
        }
    
    def _generate_empty_response_result(self, prompt_config: Dict) -> Dict[str, Any]:
        """Generate result for empty or insufficient response"""
        return {
            'prompt_id': prompt_config.get('title', 'Unknown'),
            'response_length': 0,
            'word_count': 0,
            'time_taken': 0,
            'overall_score': 0,
            'grade': "F",
            'detailed_feedback': ["No response provided - please write a response to the prompt"],
            'improvement_suggestions': [{
                'area': 'Response Completion',
                'suggestion': 'Ensure you write a complete response to all prompts',
                'priority': 'critical'
            }],
            'ml_features': {
                'communication_overall_score': 0,
                'communication_grammar_score': 0,
                'communication_clarity_score': 0,
                'communication_professionalism_score': 0,
                'communication_structure_score': 0,
                'communication_vocabulary_score': 0,
                'communication_word_count': 0,
                'communication_response_time': 0,
                'communication_vocabulary_richness': 0
            }
        }

def main():
    """Test the communication assessment engine"""
    print("📝 Testing Communication Assessment Engine")
    print("=" * 50)
    
    engine = CommunicationAssessmentEngine()
    
    # Generate a test
    test_config = engine.generate_communication_test()
    print(f"Generated test with {test_config['total_prompts']} prompts")
    
    # Test with sample response
    sample_response = """
    Dear Manager,
    
    I am writing to request a two-week extension for the current project deadline. Due to unexpected technical challenges with the database integration, we have encountered delays that were not anticipated in the original timeline.
    
    The main issue involves compatibility problems between our new system and the legacy database. My team and I have been working diligently to resolve this, but it requires additional time for thorough testing and implementation.
    
    I propose to use the additional two weeks to complete the integration properly and conduct comprehensive testing to ensure quality delivery. This will allow us to deliver a robust solution that meets all requirements.
    
    Thank you for your understanding and consideration.
    
    Best regards,
    John Smith
    """
    
    # Evaluate the response
    result = engine.evaluate_written_response(
        test_config['prompts'][0], 
        sample_response, 
        600  # 10 minutes
    )
    
    print(f"\nEvaluation Results:")
    print(f"Overall Score: {result['overall_score']:.1f}/100 (Grade: {result['grade']})")
    print(f"Word Count: {result['word_count']}")
    print(f"Grammar & Spelling: {result['grammar_spelling']['score']:.1f}/100")
    print(f"Clarity & Readability: {result['clarity_readability']['score']:.1f}/100")
    print(f"Professionalism: {result['professionalism']['score']:.1f}/100")
    
    print(f"\nFeedback:")
    for feedback in result['detailed_feedback']:
        print(f"  • {feedback}")
    
    print(f"\nImprovement Suggestions:")
    for suggestion in result['improvement_suggestions']:
        print(f"  • {suggestion['area']}: {suggestion['suggestion']}")
    
    print("\n✅ Communication Assessment Engine test completed!")

if __name__ == "__main__":
    main()