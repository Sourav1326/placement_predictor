"""
Gamified Situational Judgment Tests (SJTs) with Personality Analysis
Advanced behavioral assessment inspired by Big Tech hiring practices
"""

import json
import random
from typing import Dict, List, Any, Tuple
from datetime import datetime
import numpy as np

class SituationalJudgmentEngine:
    """Advanced SJT engine with personality analysis and gamification"""
    
    def __init__(self):
        self.scenario_bank = self._load_scenario_bank()
        self.personality_traits = self._define_personality_traits()
        self.competency_framework = self._define_competency_framework()
        
    def _load_scenario_bank(self) -> Dict[str, List[Dict]]:
        """Load comprehensive scenario bank categorized by workplace situations"""
        return {
            "conflict_resolution": [
                {
                    "id": "cr_001",
                    "title": "Code Review Disagreement",
                    "scenario": "During a code review, a senior colleague strongly disagrees with your implementation approach and becomes defensive when you point out a potential bug. The colleague says 'I've been coding for 10 years, I know what I'm doing.' The deadline is approaching, and this issue could cause system failures.",
                    "options": [
                        {
                            "text": "Escalate immediately to the team lead to avoid responsibility",
                            "traits": {"assertiveness": -2, "collaboration": -3, "leadership": -2, "problem_solving": -1},
                            "competencies": {"teamwork": 1, "communication": 2, "decision_making": 2}
                        },
                        {
                            "text": "Schedule a private one-on-one discussion to explain your concerns with specific examples and data",
                            "traits": {"assertiveness": 3, "collaboration": 3, "leadership": 3, "problem_solving": 3},
                            "competencies": {"teamwork": 5, "communication": 5, "decision_making": 4}
                        },
                        {
                            "text": "Document the issue privately and implement your own fix without telling anyone",
                            "traits": {"assertiveness": 1, "collaboration": -2, "leadership": -1, "problem_solving": 2},
                            "competencies": {"teamwork": 1, "communication": 1, "decision_making": 3}
                        }
                    ],
                    "ideal_response": 1,
                    "difficulty": "hard",
                    "workplace_relevance": "high",
                    "tags": ["conflict", "technical", "senior_colleague", "quality"]
                }
            ],
            "leadership_initiative": [
                {
                    "id": "li_001",
                    "title": "Process Improvement Initiative",
                    "scenario": "You notice that your team's current development process is inefficient and causing delays. However, changing the process would require convincing senior team members who are resistant to change.",
                    "options": [
                        {
                            "text": "Keep quiet and focus on your own work - you're too junior to suggest changes",
                            "traits": {"assertiveness": -3, "collaboration": -1, "leadership": -3, "problem_solving": -1},
                            "competencies": {"teamwork": 2, "communication": 1, "decision_making": 1}
                        },
                        {
                            "text": "Prepare a detailed proposal with data and present it to the team lead professionally",
                            "traits": {"assertiveness": 3, "collaboration": 2, "leadership": 3, "problem_solving": 3},
                            "competencies": {"teamwork": 4, "communication": 5, "decision_making": 5}
                        }
                    ],
                    "ideal_response": 1,
                    "difficulty": "hard",
                    "workplace_relevance": "high",
                    "tags": ["initiative", "change_management", "junior_leadership"]
                }
            ]
        }
    
    def _define_personality_traits(self) -> Dict[str, Dict]:
        """Define personality traits measured by SJT"""
        return {
            "assertiveness": {
                "description": "Confidence in expressing opinions and taking initiative",
                "range": [-5, 5],
                "interpretation": {
                    (-5, -2): "Passive, avoids confrontation",
                    (-1, 1): "Balanced approach, chooses battles wisely",
                    (2, 5): "Highly assertive, confident in leadership roles"
                }
            },
            "collaboration": {
                "description": "Ability to work effectively with others",
                "range": [-5, 5],
                "interpretation": {
                    (-5, -2): "Prefers working alone",
                    (-1, 1): "Good team player with balanced independence",
                    (2, 5): "Excellent collaborator, builds strong relationships"
                }
            },
            "leadership": {
                "description": "Natural tendency to take charge and guide others",
                "range": [-5, 5],
                "interpretation": {
                    (-5, -2): "Prefers following others",
                    (-1, 1): "Shows leadership when needed",
                    (2, 5): "Natural leader, takes initiative"
                }
            },
            "problem_solving": {
                "description": "Analytical thinking and solution-oriented approach",
                "range": [-5, 5],
                "interpretation": {
                    (-5, -2): "May avoid complex problems",
                    (-1, 1): "Good problem-solving skills",
                    (2, 5): "Excellent analytical skills, thrives on challenges"
                }
            }
        }
    
    def _define_competency_framework(self) -> Dict[str, Dict]:
        """Define workplace competencies measured by SJT"""
        return {
            "teamwork": {
                "description": "Ability to collaborate effectively in team environments",
                "levels": {
                    1: "Basic - Can work with others when required",
                    2: "Developing - Contributes positively to team efforts",
                    3: "Proficient - Strong team player, facilitates collaboration",
                    4: "Advanced - Builds high-performing teams",
                    5: "Expert - Exemplary team leadership and collaboration"
                }
            },
            "communication": {
                "description": "Effective verbal and written communication skills",
                "levels": {
                    1: "Basic - Can convey simple information clearly",
                    2: "Developing - Good communication in familiar contexts",
                    3: "Proficient - Communicates effectively across different audiences",
                    4: "Advanced - Persuasive and influential communicator",
                    5: "Expert - Exceptional communication leadership"
                }
            },
            "decision_making": {
                "description": "Quality of judgment and decision-making process",
                "levels": {
                    1: "Basic - Makes simple decisions with guidance",
                    2: "Developing - Good decisions in routine situations",
                    3: "Proficient - Makes sound decisions under pressure",
                    4: "Advanced - Excellent strategic decision-making",
                    5: "Expert - Exceptional judgment in complex situations"
                }
            }
        }
    
    def generate_sjt_assessment(self, focus_areas: List[str] = None, num_scenarios: int = 6) -> Dict[str, Any]:
        """Generate a comprehensive SJT assessment"""
        if focus_areas is None:
            focus_areas = list(self.scenario_bank.keys())
        
        available_scenarios = []
        for area in focus_areas:
            if area in self.scenario_bank:
                available_scenarios.extend(self.scenario_bank[area])
        
        selected_scenarios = available_scenarios[:num_scenarios]
        
        return {
            'assessment_id': f"sjt_{int(datetime.now().timestamp())}",
            'focus_areas': focus_areas,
            'scenarios': selected_scenarios,
            'total_scenarios': len(selected_scenarios),
            'estimated_time': len(selected_scenarios) * 3,
            'instructions': self._get_sjt_instructions(),
            'personality_traits_measured': list(self.personality_traits.keys()),
            'competencies_measured': list(self.competency_framework.keys())
        }
    
    def _get_sjt_instructions(self) -> List[str]:
        """Get comprehensive instructions for SJT"""
        return [
            "🎯 Situational Judgment Test - Real Workplace Scenarios",
            "You will be presented with realistic workplace situations.",
            "Choose the response that best represents what you would actually do.",
            "Consider both immediate and long-term impacts of your decisions.",
            "Your responses will help create a comprehensive personality profile."
        ]
    
    def evaluate_sjt_responses(self, assessment_config: Dict, user_responses: List[Dict]) -> Dict[str, Any]:
        """Comprehensive evaluation with personality analysis"""
        scenarios = assessment_config['scenarios']
        
        personality_scores = {trait: 0 for trait in self.personality_traits.keys()}
        competency_scores = {comp: 0 for comp in self.competency_framework.keys()}
        
        scenario_analyses = []
        total_ideal_matches = 0
        
        for i, scenario in enumerate(scenarios):
            user_response = user_responses[i] if i < len(user_responses) else None
            
            if user_response and 'selected_option' in user_response:
                selected_idx = user_response['selected_option']
                
                if 0 <= selected_idx < len(scenario['options']):
                    selected_option = scenario['options'][selected_idx]
                    is_ideal = selected_idx == scenario.get('ideal_response', -1)
                    
                    # Update scores
                    for trait, score in selected_option.get('traits', {}).items():
                        if trait in personality_scores:
                            personality_scores[trait] += score
                    
                    for competency, score in selected_option.get('competencies', {}).items():
                        if competency in competency_scores:
                            competency_scores[competency] += score
                    
                    if is_ideal:
                        total_ideal_matches += 1
                    
                    scenario_analyses.append({
                        'scenario_id': scenario['id'],
                        'scenario_title': scenario['title'],
                        'selected_option': selected_idx,
                        'is_ideal_response': is_ideal,
                        'trait_impacts': selected_option.get('traits', {}),
                        'competency_impacts': selected_option.get('competencies', {})
                    })
        
        personality_profile = self._generate_personality_profile(personality_scores)
        competency_assessment = self._generate_competency_assessment(competency_scores)
        
        overall_performance = (total_ideal_matches / len(scenarios)) * 100 if scenarios else 0
        
        return {
            'assessment_id': assessment_config['assessment_id'],
            'completion_timestamp': datetime.now().isoformat(),
            'overall_performance': round(overall_performance, 2),
            'ideal_responses': total_ideal_matches,
            'personality_profile': personality_profile,
            'competency_assessment': competency_assessment,
            'work_style_analysis': self._analyze_work_style(personality_scores),
            'career_recommendations': self._generate_career_recommendations(personality_scores),
            'scenario_analyses': scenario_analyses,
            'ml_features': self._extract_sjt_ml_features(personality_scores, competency_scores, overall_performance)
        }
    
    def _generate_personality_profile(self, personality_scores: Dict[str, int]) -> Dict[str, Any]:
        """Generate detailed personality profile"""
        profile = {}
        
        for trait, score in personality_scores.items():
            normalized_score = max(-5, min(5, score))
            percentile = max(0, min(100, ((normalized_score + 5) / 10) * 100))
            
            profile[trait] = {
                'raw_score': score,
                'normalized_score': normalized_score,
                'percentile': round(percentile, 1),
                'level': self._get_trait_level(normalized_score),
                'description': self.personality_traits[trait]['description']
            }
        
        return profile
    
    def _get_trait_level(self, normalized_score: float) -> str:
        """Convert normalized score to descriptive level"""
        if normalized_score >= 3:
            return "Very High"
        elif normalized_score >= 1:
            return "High"
        elif normalized_score >= -1:
            return "Moderate"
        else:
            return "Low"
    
    def _generate_competency_assessment(self, competency_scores: Dict[str, int]) -> Dict[str, Any]:
        """Generate detailed competency assessment"""
        assessment = {}
        
        for competency, score in competency_scores.items():
            level = max(1, min(5, int((score / 5) + 3)))
            
            assessment[competency] = {
                'raw_score': score,
                'level': level,
                'level_description': self.competency_framework[competency]['levels'].get(level, "Developing"),
                'description': self.competency_framework[competency]['description'],
                'strength_area': level >= 4
            }
        
        return assessment
    
    def _analyze_work_style(self, personality_scores: Dict) -> Dict[str, str]:
        """Analyze work style based on personality patterns"""
        leadership_score = personality_scores.get('leadership', 0)
        collaboration_score = personality_scores.get('collaboration', 0)
        assertiveness_score = personality_scores.get('assertiveness', 0)
        
        if leadership_score >= 2 and assertiveness_score >= 2:
            primary_style = "Natural Leader"
        elif collaboration_score >= 2:
            primary_style = "Team Collaborator"
        elif assertiveness_score <= -1:
            primary_style = "Supportive Contributor"
        else:
            primary_style = "Balanced Professional"
        
        return {
            'primary_work_style': primary_style,
            'communication_style': "Direct" if assertiveness_score >= 2 else "Collaborative",
            'team_role_preference': "Leadership Role" if leadership_score >= 2 else "Team Member"
        }
    
    def _generate_career_recommendations(self, personality_scores: Dict) -> List[str]:
        """Generate career fit recommendations"""
        recommendations = []
        
        leadership = personality_scores.get('leadership', 0)
        collaboration = personality_scores.get('collaboration', 0)
        problem_solving = personality_scores.get('problem_solving', 0)
        
        if leadership >= 2 and problem_solving >= 2:
            recommendations.append("Technical Leadership roles (Team Lead, Engineering Manager)")
        if collaboration >= 2:
            recommendations.append("Cross-functional roles (Product Manager, DevOps Engineer)")
        if problem_solving >= 2:
            recommendations.append("Analytical roles (Software Architect, Data Scientist)")
        
        if not recommendations:
            recommendations.append("Individual Contributor roles with growth potential")
        
        return recommendations
    
    def _extract_sjt_ml_features(self, personality_scores: Dict, competency_scores: Dict, overall_performance: float) -> Dict[str, float]:
        """Extract features for ML model integration"""
        features = {
            'sjt_overall_performance': overall_performance,
            'sjt_assertiveness_score': personality_scores.get('assertiveness', 0),
            'sjt_collaboration_score': personality_scores.get('collaboration', 0),
            'sjt_leadership_score': personality_scores.get('leadership', 0),
            'sjt_problem_solving_score': personality_scores.get('problem_solving', 0),
            'sjt_teamwork_competency': competency_scores.get('teamwork', 0),
            'sjt_communication_competency': competency_scores.get('communication', 0),
            'sjt_decision_making_competency': competency_scores.get('decision_making', 0)
        }
        
        return features

def main():
    """Test the SJT engine"""
    print("🎯 Testing Situational Judgment Test Engine")
    print("=" * 50)
    
    engine = SituationalJudgmentEngine()
    
    # Generate assessment
    assessment = engine.generate_sjt_assessment(num_scenarios=2)
    print(f"Generated SJT with {assessment['total_scenarios']} scenarios")
    
    # Simulate responses
    sample_responses = [
        {'selected_option': 1, 'response_time': 120},
        {'selected_option': 0, 'response_time': 90}
    ]
    
    # Evaluate
    results = engine.evaluate_sjt_responses(assessment, sample_responses)
    
    print(f"\nResults:")
    print(f"Overall Performance: {results['overall_performance']:.1f}%")
    print(f"Primary Work Style: {results['work_style_analysis']['primary_work_style']}")
    print(f"Career Recommendations: {results['career_recommendations']}")
    
    print("\n✅ SJT Engine test completed!")

if __name__ == "__main__":
    main()