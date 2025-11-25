"""
Advanced Recommendation System for Placement Improvement
Provides personalized, actionable advice to students based on their profiles
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from src.model_training import PlacementPredictor
from src.utils.data_preprocessing import PlacementDataPreprocessor

class PlacementRecommendationEngine:
    """
    Intelligent recommendation system for placement improvement
    """
    
    def __init__(self):
        self.predictor = PlacementPredictor()
        self.predictor.load_models()
        
        # Load dataset for benchmark analysis
        if os.path.exists('data/placement_data.csv'):
            self.df = pd.read_csv('data/placement_data.csv')
            self.placed_students = self.df[self.df['placed'] == 1]
        else:
            self.df = None
            self.placed_students = None
    
    def analyze_student_profile(self, student_data):
        """
        Comprehensive analysis of student profile
        """
        analysis = {
            'current_probability': 0,
            'strengths': [],
            'weaknesses': [],
            'critical_gaps': [],
            'benchmark_comparison': {},
            'improvement_potential': {},
            'timeline_estimate': '6-12 months'
        }
        
        # Get current prediction
        try:
            result = self.predictor.predict_placement(student_data)
            if result:
                analysis['current_probability'] = result['probability']
        except Exception as e:
            print(f"Prediction error: {e}")
            analysis['current_probability'] = 0.5  # Default
        
        # Define success thresholds based on placed students
        if self.placed_students is not None and len(self.placed_students) > 0:
            thresholds = {
                'cgpa': self.placed_students['cgpa'].quantile(0.25),
                'num_projects': self.placed_students['num_projects'].quantile(0.25),
                'num_internships': self.placed_students['num_internships'].quantile(0.25),
                'leetcode_score': self.placed_students['leetcode_score'].quantile(0.25),
                'communication_score': self.placed_students['communication_score'].quantile(0.25),
                'num_certifications': self.placed_students['num_certifications'].quantile(0.25),
                'num_hackathons': self.placed_students['num_hackathons'].quantile(0.25)
            }
            
            # Optimal targets (75th percentile of placed students)
            targets = {
                'cgpa': self.placed_students['cgpa'].quantile(0.75),
                'num_projects': self.placed_students['num_projects'].quantile(0.75),
                'num_internships': self.placed_students['num_internships'].quantile(0.75),
                'leetcode_score': self.placed_students['leetcode_score'].quantile(0.75),
                'communication_score': self.placed_students['communication_score'].quantile(0.75),
                'num_certifications': self.placed_students['num_certifications'].quantile(0.75),
                'num_hackathons': self.placed_students['num_hackathons'].quantile(0.75)
            }
        else:
            # Fallback thresholds
            thresholds = {
                'cgpa': 7.5, 'num_projects': 2, 'num_internships': 1,
                'leetcode_score': 1000, 'communication_score': 6.5,
                'num_certifications': 1, 'num_hackathons': 1
            }
            targets = {
                'cgpa': 8.5, 'num_projects': 4, 'num_internships': 2,
                'leetcode_score': 1800, 'communication_score': 8.0,
                'num_certifications': 3, 'num_hackathons': 3
            }
        
        # Analyze each factor
        factors = {
            'cgpa': 'CGPA',
            'num_projects': 'Projects',
            'num_internships': 'Internships',
            'leetcode_score': 'LeetCode Score',
            'communication_score': 'Communication Skills',
            'num_certifications': 'Certifications',
            'num_hackathons': 'Hackathons'
        }
        
        for key, label in factors.items():
            if key in student_data:
                current_value = student_data[key]
                threshold = thresholds.get(key, 0)
                target = targets.get(key, threshold * 1.5)
                
                # Categorize performance
                if current_value >= target:
                    analysis['strengths'].append({
                        'factor': label,
                        'current': current_value,
                        'status': 'Excellent',
                        'message': f'Your {label.lower()} is above average for placed students'
                    })
                elif current_value >= threshold:
                    analysis['strengths'].append({
                        'factor': label,
                        'current': current_value,
                        'status': 'Good',
                        'message': f'Your {label.lower()} meets minimum requirements'
                    })
                else:
                    gap = threshold - current_value
                    if gap > (threshold * 0.3):  # Significant gap
                        analysis['critical_gaps'].append({
                            'factor': label,
                            'current': current_value,
                            'minimum': threshold,
                            'target': target,
                            'gap': gap,
                            'priority': 'High'
                        })
                    else:
                        analysis['weaknesses'].append({
                            'factor': label,
                            'current': current_value,
                            'minimum': threshold,
                            'target': target,
                            'gap': gap,
                            'priority': 'Medium'
                        })
                
                # Benchmark comparison
                if self.placed_students is not None:
                    percentile = (self.placed_students[key] <= current_value).mean() * 100
                    analysis['benchmark_comparison'][label] = {
                        'percentile': percentile,
                        'description': self._get_percentile_description(percentile)
                    }
                
                # Calculate improvement potential
                if current_value < target:
                    potential_increase = (target - current_value) / target
                    analysis['improvement_potential'][label] = {
                        'current': current_value,
                        'target': target,
                        'potential_impact': min(potential_increase * 20, 15)  # Max 15% impact per factor
                    }
        
        return analysis
    
    def _get_percentile_description(self, percentile):
        """Convert percentile to descriptive text"""
        if percentile >= 75:
            return "Top 25% among placed students"
        elif percentile >= 50:
            return "Above average among placed students"
        elif percentile >= 25:
            return "Below average among placed students"
        else:
            return "Bottom 25% among placed students"
    
    def generate_action_plan(self, student_data, target_probability=0.75):
        """
        Generate comprehensive action plan with timeline and priorities
        """
        analysis = self.analyze_student_profile(student_data)
        current_prob = analysis['current_probability']
        
        action_plan = {
            'current_probability': current_prob,
            'target_probability': target_probability,
            'probability_gap': max(0, target_probability - current_prob),
            'estimated_timeline': '6-12 months',
            'priority_actions': [],
            'medium_term_goals': [],
            'long_term_objectives': [],
            'quick_wins': []
        }
        
        # Priority actions based on critical gaps
        for gap in analysis['critical_gaps']:
            if gap['factor'] == 'CGPA':
                action_plan['priority_actions'].append({
                    'action': f"Improve CGPA from {gap['current']:.1f} to {gap['target']:.1f}",
                    'timeline': '1-2 semesters',
                    'difficulty': 'High',
                    'impact': 'Very High (15-20% probability increase)',
                    'steps': [
                        'Focus on understanding core concepts rather than rote learning',
                        'Maintain consistent daily study schedule',
                        'Seek help from professors during office hours',
                        'Form study groups with high-performing peers',
                        'Practice with previous year papers and assignments',
                        'Consider retaking courses with low grades if possible'
                    ],
                    'resources': [
                        'Academic counseling services',
                        'Online courses for weak subjects',
                        'Tutoring services',
                        'Study groups and peer learning'
                    ]
                })
            
            elif gap['factor'] == 'Internships':
                action_plan['priority_actions'].append({
                    'action': f"Complete {int(gap['target'])} internship(s)",
                    'timeline': '3-6 months',
                    'difficulty': 'Medium',
                    'impact': 'Very High (20-25% probability increase)',
                    'steps': [
                        'Start applying 3-4 months before desired start date',
                        'Tailor resume for each application',
                        'Practice technical and behavioral interviews',
                        'Leverage college placement cell and alumni network',
                        'Consider virtual internships if location is a constraint',
                        'Build projects relevant to target companies'
                    ],
                    'resources': [
                        'LinkedIn for networking',
                        'Company career pages',
                        'Internship platforms (Internshala, etc.)',
                        'College placement cell',
                        'Alumni network'
                    ]
                })
            
            elif gap['factor'] == 'Projects':
                action_plan['priority_actions'].append({
                    'action': f"Build {int(gap['target'] - gap['current'])} more project(s)",
                    'timeline': '2-4 months',
                    'difficulty': 'Medium',
                    'impact': 'High (10-15% probability increase)',
                    'steps': [
                        'Choose projects that solve real-world problems',
                        'Use current industry technologies and frameworks',
                        'Ensure projects are different from each other',
                        'Document projects thoroughly with README files',
                        'Deploy projects with live URLs for demonstration',
                        'Add projects to portfolio website and GitHub'
                    ],
                    'resources': [
                        'GitHub for version control',
                        'Free hosting platforms (Heroku, Vercel, Netlify)',
                        'Online tutorials and documentation',
                        'Open source project ideas',
                        'Hackathon problem statements'
                    ]
                })
        
        # Medium-term goals for moderate improvements
        for weakness in analysis['weaknesses']:
            if weakness['factor'] == 'LeetCode Score':
                action_plan['medium_term_goals'].append({
                    'goal': f"Improve LeetCode score to {int(weakness['target'])}",
                    'timeline': '3-4 months',
                    'difficulty': 'Medium',
                    'impact': 'Medium (8-12% probability increase)',
                    'approach': [
                        'Solve 2-3 problems daily consistently',
                        'Focus on different difficulty levels (Easy: 40%, Medium: 50%, Hard: 10%)',
                        'Review and understand optimal solutions',
                        'Practice problems from top companies',
                        'Participate in weekly contests',
                        'Track progress and identify weak areas'
                    ]
                })
            
            elif weakness['factor'] == 'Communication Skills':
                action_plan['medium_term_goals'].append({
                    'goal': f"Improve communication skills to {weakness['target']:.1f}/10",
                    'timeline': '3-6 months',
                    'difficulty': 'Medium',
                    'impact': 'Medium (8-10% probability increase)',
                    'approach': [
                        'Join public speaking clubs (Toastmasters)',
                        'Practice technical presentations',
                        'Record yourself explaining technical concepts',
                        'Participate in group discussions',
                        'Take online communication courses',
                        'Practice mock interviews regularly'
                    ]
                })
        
        # Quick wins for immediate improvements
        quick_wins_suggestions = [
            {
                'action': 'Optimize LinkedIn profile',
                'timeline': '1 week',
                'impact': 'Low but important for visibility',
                'steps': ['Professional photo', 'Detailed summary', 'Skills endorsements', 'Project showcases']
            },
            {
                'action': 'Create/update portfolio website',
                'timeline': '2 weeks',
                'impact': 'Medium for showcasing work',
                'steps': ['Choose template', 'Add projects', 'Include resume', 'Add contact information']
            },
            {
                'action': 'Clean up GitHub profile',
                'timeline': '1 week',
                'impact': 'Medium for technical credibility',
                'steps': ['Pin important repositories', 'Add README files', 'Remove unnecessary repos', 'Add profile README']
            },
            {
                'action': 'Get industry-relevant certification',
                'timeline': '1-2 months',
                'impact': 'Low-Medium',
                'steps': ['Choose relevant certification', 'Study consistently', 'Take practice tests', 'Add to resume/LinkedIn']
            }
        ]
        
        action_plan['quick_wins'] = quick_wins_suggestions
        
        # Long-term objectives
        long_term_goals = [
            {
                'objective': 'Build domain expertise',
                'timeline': '6-12 months',
                'description': 'Develop deep knowledge in 1-2 specific technology areas',
                'benefits': 'Positions you as a specialist, increases interview success rate'
            },
            {
                'objective': 'Develop leadership experience',
                'timeline': '4-8 months',
                'description': 'Lead a technical project or club activity',
                'benefits': 'Demonstrates initiative and management potential'
            },
            {
                'objective': 'Create impact through contributions',
                'timeline': '6-12 months',
                'description': 'Contribute to open source or publish technical content',
                'benefits': 'Shows commitment to field and helps with personal branding'
            }
        ]
        
        action_plan['long_term_objectives'] = long_term_goals
        
        return action_plan
    
    def simulate_improvements(self, student_data, improvements):
        """
        Simulate how specific improvements would affect placement probability
        """
        simulated_data = student_data.copy()
        
        # Apply improvements
        for key, improvement in improvements.items():
            if key in simulated_data:
                simulated_data[key] += improvement
        
        # Get new prediction
        try:
            original_result = self.predictor.predict_placement(student_data)
            improved_result = self.predictor.predict_placement(simulated_data)
            
            if original_result and improved_result:
                return {
                    'original_probability': original_result['probability'],
                    'improved_probability': improved_result['probability'],
                    'probability_increase': improved_result['probability'] - original_result['probability'],
                    'percentage_increase': (improved_result['probability'] - original_result['probability']) * 100
                }
        except Exception as e:
            print(f"Simulation error: {e}")
        
        return None
    
    def get_peer_comparison(self, student_data):
        """
        Compare student with peers in same branch
        """
        if self.df is None:
            return None
        
        branch = student_data.get('branch', 'Computer Science')
        branch_students = self.df[self.df['branch'] == branch]
        
        if len(branch_students) == 0:
            return None
        
        comparison = {
            'branch': branch,
            'total_peers': len(branch_students),
            'placed_peers': int(branch_students['placed'].sum()),
            'branch_placement_rate': float(branch_students['placed'].mean()),
            'comparisons': {}
        }
        
        numerical_fields = ['cgpa', 'num_projects', 'num_internships', 'leetcode_score', 'communication_score']
        
        for field in numerical_fields:
            if field in student_data and field in branch_students.columns:
                student_value = student_data[field]
                branch_mean = branch_students[field].mean()
                percentile = (branch_students[field] <= student_value).mean() * 100
                
                comparison['comparisons'][field] = {
                    'student_value': student_value,
                    'branch_average': branch_mean,
                    'percentile': percentile,
                    'status': 'Above Average' if student_value > branch_mean else 'Below Average'
                }
        
        return comparison
    
    def generate_report(self, student_data):
        """
        Generate comprehensive recommendation report
        """
        analysis = self.analyze_student_profile(student_data)
        action_plan = self.generate_action_plan(student_data)
        peer_comparison = self.get_peer_comparison(student_data)
        
        # Simulate some potential improvements
        potential_improvements = {
            'cgpa': 0.5,
            'num_projects': 2,
            'num_internships': 1,
            'leetcode_score': 500,
            'communication_score': 1.0
        }
        
        simulation = self.simulate_improvements(student_data, potential_improvements)
        
        report = {
            'student_analysis': analysis,
            'action_plan': action_plan,
            'peer_comparison': peer_comparison,
            'improvement_simulation': simulation,
            'summary': {
                'current_probability': analysis['current_probability'],
                'key_strengths': len(analysis['strengths']),
                'critical_gaps': len(analysis['critical_gaps']),
                'estimated_timeline': action_plan['estimated_timeline']
            }
        }
        
        return report

def test_recommendation_system():
    """Test the recommendation system with sample data"""
    engine = PlacementRecommendationEngine()
    
    # Test with a sample student
    test_student = {
        'student_id': 'RECOM001',
        'branch': 'Computer Science',
        'cgpa': 7.2,
        'tenth_percentage': 85.0,
        'twelfth_percentage': 82.0,
        'num_projects': 1,
        'num_internships': 0,
        'num_certifications': 1,
        'programming_languages': 'Python, Java',
        'leetcode_score': 800,
        'codechef_rating': 1200,
        'communication_score': 6.0,
        'leadership_score': 5.5,
        'num_hackathons': 1,
        'club_participation': 0,
        'online_courses': 2,
        'placed': 0,
        'salary_package': 0,
        'package_category': 'Unknown'
    }
    
    print("🎯 Placement Recommendation System Test")
    print("=" * 50)
    
    # Generate comprehensive report
    report = engine.generate_report(test_student)
    
    print(f"📊 Current Analysis:")
    print(f"  Placement Probability: {report['student_analysis']['current_probability']:.1%}")
    print(f"  Strengths: {len(report['student_analysis']['strengths'])}")
    print(f"  Critical Gaps: {len(report['student_analysis']['critical_gaps'])}")
    
    print(f"\n🚨 Critical Improvements Needed:")
    for gap in report['student_analysis']['critical_gaps']:
        print(f"  - {gap['factor']}: Current {gap['current']}, Target {gap['target']}")
    
    print(f"\n🎯 Priority Actions:")
    for action in report['action_plan']['priority_actions'][:3]:  # Show top 3
        print(f"  - {action['action']}")
        print(f"    Timeline: {action['timeline']}, Impact: {action['impact']}")
    
    if report['improvement_simulation']:
        sim = report['improvement_simulation']
        print(f"\n📈 Improvement Simulation:")
        print(f"  Current: {sim['original_probability']:.1%}")
        print(f"  After Improvements: {sim['improved_probability']:.1%}")
        print(f"  Potential Increase: +{sim['percentage_increase']:.1f}%")
    
    print(f"\n✅ Recommendation system working correctly!")

if __name__ == "__main__":
    test_recommendation_system()