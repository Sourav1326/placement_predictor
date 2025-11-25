"""
Company & Role Prediction System with Tier Classification
Predicts specific companies and tiers based on student profiles
"""

import sqlite3
import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompanyRolePredictionEngine:
    """Predicts company tiers and specific roles for students"""
    
    def __init__(self, db_path: str = "placement_predictor.db"):
        self.db_path = db_path
        self.setup_prediction_database()
        
        # Company tier definitions
        self.company_tiers = {
            'tier_1': {
                'name': 'Top Product Companies',
                'companies': ['Google', 'Microsoft', 'Amazon', 'Meta', 'Netflix', 'Apple'],
                'salary_range': '₹15-50+ LPA',
                'requirements': {
                    'min_cgpa': 8.0,
                    'required_skills': ['python', 'java', 'algorithms', 'data structures'],
                    'coding_threshold': 85
                }
            },
            'tier_2': {
                'name': 'Large MNCs & Services',
                'companies': ['TCS', 'Infosys', 'Wipro', 'Capgemini', 'Accenture', 'Cognizant'],
                'salary_range': '₹3.5-12 LPA',
                'requirements': {
                    'min_cgpa': 6.5,
                    'required_skills': ['java', 'sql', 'web development'],
                    'coding_threshold': 60
                }
            },
            'tier_3': {
                'name': 'Startups & Growth Companies',
                'companies': ['Zomato', 'Paytm', 'Swiggy', 'Flipkart', 'Ola', 'Razorpay'],
                'salary_range': '₹4-15 LPA',
                'requirements': {
                    'min_cgpa': 7.0,
                    'required_skills': ['python', 'javascript', 'react', 'node.js'],
                    'coding_threshold': 70
                }
            }
        }
    
    def setup_prediction_database(self):
        """Initialize prediction tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Live job openings
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS live_job_openings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_title TEXT NOT NULL,
                    company_name TEXT NOT NULL,
                    company_tier TEXT,
                    location TEXT,
                    experience_required TEXT,
                    skills_required TEXT,
                    salary_range TEXT,
                    application_link TEXT,
                    posted_date DATE,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # Prediction cache
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS prediction_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    prediction_results TEXT,
                    confidence_score REAL,
                    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Populate sample job data
            cursor.execute("SELECT COUNT(*) FROM live_job_openings")
            if cursor.fetchone()[0] == 0:
                self._populate_job_openings(cursor)
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Database setup error: {e}")
    
    def _populate_job_openings(self, cursor):
        """Add sample job openings"""
        jobs = [
            ('Software Developer', 'TCS', 'tier_2', 'Bangalore', '0-2 years', 
             '["java", "sql", "spring_boot"]', '₹4-7 LPA', 'https://tcs.com/careers', '2025-01-10'),
            
            ('Frontend Developer', 'Infosys', 'tier_2', 'Pune', '1-3 years',
             '["react", "javascript", "html", "css"]', '₹5-9 LPA', 'https://infosys.com/careers', '2025-01-12'),
            
            ('Backend Developer', 'Zomato', 'tier_3', 'Gurgaon', '1-4 years',
             '["python", "django", "postgresql"]', '₹8-15 LPA', 'https://zomato.com/careers', '2025-01-09'),
            
            ('Software Engineer', 'Microsoft', 'tier_1', 'Hyderabad', '0-2 years',
             '["c#", "azure", "algorithms"]', '₹18-35 LPA', 'https://microsoft.com/careers', '2025-01-08'),
            
            ('Data Analyst', 'Wipro', 'tier_2', 'Chennai', '0-2 years',
             '["sql", "python", "excel"]', '₹4-8 LPA', 'https://wipro.com/careers', '2025-01-11'),
            
            ('Full Stack Developer', 'Paytm', 'tier_3', 'Noida', '1-3 years',
             '["react", "node.js", "mongodb"]', '₹6-12 LPA', 'https://paytm.com/careers', '2025-01-13')
        ]
        
        cursor.executemany('''
            INSERT INTO live_job_openings 
            (job_title, company_name, company_tier, location, experience_required, 
             skills_required, salary_range, application_link, posted_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', jobs)
    
    def predict_company_tiers(self, user_id: int) -> Dict[str, Any]:
        """Predict company tiers and provide recommendations"""
        try:
            user_profile = self._get_user_profile(user_id)
            
            if not user_profile:
                return {'success': False, 'error': 'User profile not found'}
            
            # Calculate tier probabilities
            tier_predictions = {}
            
            for tier_name, tier_info in self.company_tiers.items():
                probability = self._calculate_tier_probability(user_profile, tier_info)
                tier_predictions[tier_name] = {
                    'probability': probability,
                    'tier_name': tier_info['name'],
                    'salary_range': tier_info['salary_range'],
                    'sample_companies': tier_info['companies'][:4],
                    'match_analysis': self._analyze_tier_match(user_profile, tier_info)
                }
            
            # Get best tier
            best_tier = max(tier_predictions.keys(), key=lambda x: tier_predictions[x]['probability'])
            
            # Get live job matches
            job_matches = self._find_matching_live_jobs(user_profile)
            
            # Get role predictions
            role_predictions = self._predict_suitable_roles(user_profile)
            
            result = {
                'success': True,
                'user_id': user_id,
                'tier_predictions': tier_predictions,
                'best_matching_tier': best_tier,
                'confidence_score': tier_predictions[best_tier]['probability'],
                'role_predictions': role_predictions,
                'live_job_matches': job_matches,
                'prediction_summary': {
                    'recommended_tier': tier_predictions[best_tier]['tier_name'],
                    'expected_salary': tier_predictions[best_tier]['salary_range'],
                    'top_companies': tier_predictions[best_tier]['sample_companies'],
                    'generated_at': datetime.now().isoformat()
                }
            }
            
            # Cache prediction
            self._cache_prediction(user_id, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _get_user_profile(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive user profile"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Basic profile
            cursor.execute('''
                SELECT skills, cgpa, experience_level, projects
                FROM student_profiles WHERE user_id = ?
            ''', (user_id,))
            
            profile_data = cursor.fetchone()
            
            if not profile_data:
                return None
            
            # Assessment scores
            cursor.execute('''
                SELECT assessment_type, score
                FROM assessment_results WHERE user_id = ?
                ORDER BY taken_at DESC
            ''', (user_id,))
            
            assessments = dict(cursor.fetchall())
            
            # Verified skills
            cursor.execute('''
                SELECT skill_name, badge_level, score
                FROM verified_skill_badges WHERE user_id = ?
            ''', (user_id,))
            
            verified_skills = cursor.fetchall()
            
            conn.close()
            
            return {
                'user_id': user_id,
                'skills': json.loads(profile_data[0]) if profile_data[0] else [],
                'cgpa': profile_data[1] or 0.0,
                'experience_level': profile_data[2] or 'beginner',
                'projects': json.loads(profile_data[3]) if profile_data[3] else [],
                'assessment_scores': assessments,
                'verified_skills': [
                    {'skill': vs[0], 'level': vs[1], 'score': vs[2]} 
                    for vs in verified_skills
                ]
            }
            
        except Exception as e:
            logger.error(f"Profile retrieval error: {e}")
            return None
    
    def _calculate_tier_probability(self, user_profile: Dict, tier_info: Dict) -> float:
        """Calculate probability of success in tier"""
        try:
            score = 0.0
            
            # CGPA check (25%)
            user_cgpa = user_profile.get('cgpa', 0.0)
            required_cgpa = tier_info['requirements']['min_cgpa']
            
            if user_cgpa >= required_cgpa:
                score += 0.25
            elif user_cgpa >= (required_cgpa - 0.5):
                score += 0.20
            elif user_cgpa >= (required_cgpa - 1.0):
                score += 0.15
            
            # Skills match (40%)
            user_skills = set(skill.lower() for skill in user_profile.get('skills', []))
            required_skills = set(skill.lower() for skill in tier_info['requirements']['required_skills'])
            
            skill_match = len(user_skills & required_skills) / len(required_skills) if required_skills else 0
            score += skill_match * 0.40
            
            # Verified skills bonus (20%)
            verified_skills = set(vs['skill'].lower() for vs in user_profile.get('verified_skills', []))
            verified_match = len(verified_skills & required_skills) / len(required_skills) if required_skills else 0
            score += verified_match * 0.20
            
            # Coding assessment (15%)
            coding_score = user_profile.get('assessment_scores', {}).get('coding_test', 0)
            coding_threshold = tier_info['requirements']['coding_threshold']
            
            if coding_score >= coding_threshold:
                score += 0.15
            elif coding_score >= (coding_threshold - 10):
                score += 0.10
            elif coding_score >= (coding_threshold - 20):
                score += 0.05
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Tier probability error: {e}")
            return 0.0
    
    def _analyze_tier_match(self, user_profile: Dict, tier_info: Dict) -> Dict[str, Any]:
        """Analyze tier compatibility"""
        try:
            strengths = []
            gaps = []
            
            # CGPA analysis
            user_cgpa = user_profile.get('cgpa', 0.0)
            required_cgpa = tier_info['requirements']['min_cgpa']
            
            if user_cgpa >= required_cgpa:
                strengths.append(f"CGPA meets requirement ({user_cgpa:.1f})")
            else:
                gaps.append(f"CGPA gap: {required_cgpa - user_cgpa:.1f} points needed")
            
            # Skills analysis
            user_skills = set(skill.lower() for skill in user_profile.get('skills', []))
            required_skills = set(skill.lower() for skill in tier_info['requirements']['required_skills'])
            
            matching = user_skills & required_skills
            missing = required_skills - user_skills
            
            if matching:
                strengths.append(f"Has required skills: {', '.join(matching)}")
            
            if missing:
                gaps.append(f"Missing skills: {', '.join(missing)}")
            
            # Assessment analysis
            coding_score = user_profile.get('assessment_scores', {}).get('coding_test', 0)
            coding_threshold = tier_info['requirements']['coding_threshold']
            
            if coding_score >= coding_threshold:
                strengths.append(f"Coding score meets threshold ({coding_score}%)")
            else:
                gaps.append(f"Coding improvement needed: {coding_threshold - coding_score}% gap")
            
            return {
                'strengths': strengths,
                'gaps': gaps,
                'overall_readiness': 'Ready' if len(gaps) == 0 else 'Needs Improvement'
            }
            
        except Exception as e:
            logger.error(f"Tier analysis error: {e}")
            return {'strengths': [], 'gaps': [], 'overall_readiness': 'Unknown'}
    
    def _find_matching_live_jobs(self, user_profile: Dict) -> List[Dict[str, Any]]:
        """Find live jobs that match user profile"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT job_title, company_name, company_tier, location, 
                       skills_required, salary_range, application_link
                FROM live_job_openings 
                WHERE is_active = 1
                ORDER BY posted_date DESC
            ''', )
            
            jobs = cursor.fetchall()
            conn.close()
            
            user_skills = set(skill.lower() for skill in user_profile.get('skills', []))
            matching_jobs = []
            
            for job in jobs:
                job_skills = set(skill.lower() for skill in json.loads(job[4]))
                
                # Calculate match score
                skill_overlap = len(user_skills & job_skills)
                match_score = skill_overlap / len(job_skills) if job_skills else 0
                
                if match_score > 0.3:  # At least 30% skill match
                    matching_jobs.append({
                        'job_title': job[0],
                        'company_name': job[1],
                        'company_tier': job[2],
                        'location': job[3],
                        'salary_range': job[5],
                        'application_link': job[6],
                        'match_score': round(match_score, 2),
                        'matching_skills': list(user_skills & job_skills),
                        'missing_skills': list(job_skills - user_skills),
                        'fit_level': self._get_fit_level(match_score)
                    })
            
            # Sort by match score
            matching_jobs.sort(key=lambda x: x['match_score'], reverse=True)
            
            return matching_jobs[:8]  # Return top 8 matches
            
        except Exception as e:
            logger.error(f"Job matching error: {e}")
            return []
    
    def _predict_suitable_roles(self, user_profile: Dict) -> List[Dict[str, Any]]:
        """Predict suitable job roles based on skills"""
        try:
            user_skills = set(skill.lower() for skill in user_profile.get('skills', []))
            
            # Role definitions
            roles = {
                'Software Developer': {
                    'required_skills': ['python', 'java', 'javascript', 'sql'],
                    'description': 'Develop software applications and systems'
                },
                'Data Analyst': {
                    'required_skills': ['sql', 'python', 'excel', 'data analysis'],
                    'description': 'Analyze data to generate business insights'
                },
                'Frontend Developer': {
                    'required_skills': ['javascript', 'react', 'html', 'css'],
                    'description': 'Build user interfaces and web applications'
                },
                'Backend Developer': {
                    'required_skills': ['python', 'java', 'sql', 'api development'],
                    'description': 'Develop server-side applications and APIs'
                },
                'QA Engineer': {
                    'required_skills': ['testing', 'automation', 'java', 'selenium'],
                    'description': 'Ensure software quality through testing'
                }
            }
            
            role_predictions = []
            
            for role_name, role_info in roles.items():
                role_skills = set(skill.lower() for skill in role_info['required_skills'])
                
                # Calculate suitability
                skill_match = len(user_skills & role_skills) / len(role_skills)
                
                if skill_match > 0.25:  # At least 25% skill match
                    role_predictions.append({
                        'role_name': role_name,
                        'suitability_score': round(skill_match, 2),
                        'description': role_info['description'],
                        'matching_skills': list(user_skills & role_skills),
                        'skill_gaps': list(role_skills - user_skills),
                        'readiness_level': self._get_readiness_level(skill_match)
                    })
            
            # Sort by suitability
            role_predictions.sort(key=lambda x: x['suitability_score'], reverse=True)
            
            return role_predictions[:5]  # Return top 5 roles
            
        except Exception as e:
            logger.error(f"Role prediction error: {e}")
            return []
    
    def _get_fit_level(self, match_score: float) -> str:
        """Convert match score to fit level"""
        if match_score >= 0.8:
            return "Excellent Fit"
        elif match_score >= 0.6:
            return "Good Fit"
        elif match_score >= 0.4:
            return "Moderate Fit"
        else:
            return "Low Fit"
    
    def _get_readiness_level(self, suitability_score: float) -> str:
        """Convert suitability to readiness level"""
        if suitability_score >= 0.8:
            return "Highly Ready"
        elif suitability_score >= 0.6:
            return "Ready"
        elif suitability_score >= 0.4:
            return "Partially Ready"
        else:
            return "Needs Preparation"
    
    def _cache_prediction(self, user_id: int, result: Dict[str, Any]):
        """Cache prediction results"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO prediction_cache 
                (user_id, prediction_results, confidence_score)
                VALUES (?, ?, ?)
            ''', (user_id, json.dumps(result), result.get('confidence_score', 0.0)))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Cache error: {e}")

# Example usage
if __name__ == "__main__":
    engine = CompanyRolePredictionEngine()
    result = engine.predict_company_tiers(user_id=1)
    print(f"Prediction Results: {result}")