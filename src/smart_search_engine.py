"""
Smart Search Panel with Personalized Results
Advanced search across learning resources, skill tests, and job openings
"""

import re
import sqlite3
from datetime import datetime
from typing import Dict, List, Any, Optional
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SmartSearchEngine:
    """Intelligent search with personalized results and actionable recommendations"""
    
    def __init__(self, db_path: str = "placement_predictor.db"):
        self.db_path = db_path
        self.setup_search_database()
    
    def setup_search_database(self):
        """Initialize search tables with sample data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Learning resources table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learning_resources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    content_type TEXT,
                    skill_tags TEXT,
                    difficulty_level TEXT,
                    duration_minutes INTEGER,
                    rating REAL DEFAULT 0.0,
                    url TEXT
                )
            ''')
            
            # Skill tests catalog
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS skill_tests_catalog (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_name TEXT NOT NULL,
                    test_type TEXT,
                    difficulty TEXT,
                    estimated_time INTEGER,
                    description TEXT,
                    badge_level TEXT
                )
            ''')
            
            # Search analytics
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS search_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    search_query TEXT,
                    results_count INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Populate sample data if empty
            cursor.execute("SELECT COUNT(*) FROM learning_resources")
            if cursor.fetchone()[0] == 0:
                self._populate_sample_data(cursor)
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Database setup error: {e}")
    
    def _populate_sample_data(self, cursor):
        """Add sample learning resources and skill tests"""
        
        # Sample learning resources
        resources = [
            ("Python for Beginners", "Complete Python course", "course", '["python", "programming"]', "beginner", 480, 4.5, "https://example.com/python"),
            ("Advanced SQL Queries", "Master complex SQL", "course", '["sql", "database"]', "advanced", 240, 4.7, "https://example.com/sql"),
            ("React.js Fundamentals", "Build modern web apps", "course", '["react", "javascript"]', "intermediate", 360, 4.6, "https://example.com/react"),
            ("Machine Learning Basics", "Introduction to ML", "course", '["machine learning", "python"]', "beginner", 600, 4.3, "https://example.com/ml"),
            ("UI/UX Design Principles", "Create user-friendly interfaces", "course", '["ui/ux", "design"]', "beginner", 180, 4.5, "https://example.com/ux")
        ]
        
        cursor.executemany('''
            INSERT INTO learning_resources 
            (title, description, content_type, skill_tags, difficulty_level, duration_minutes, rating, url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', resources)
        
        # Sample skill tests
        tests = [
            ("Python", "coding", "beginner", 30, "Basic Python programming test", "basic"),
            ("SQL", "sql", "intermediate", 45, "SQL queries and operations", "verified"),
            ("React", "framework", "intermediate", 40, "React components and hooks", "verified"),
            ("Java", "coding", "intermediate", 50, "Java programming fundamentals", "verified"),
            ("Machine Learning", "conceptual", "advanced", 90, "ML algorithms and theory", "expert")
        ]
        
        cursor.executemany('''
            INSERT INTO skill_tests_catalog 
            (skill_name, test_type, difficulty, estimated_time, description, badge_level)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', tests)
    
    def search_all(self, query: str, user_id: int, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Perform comprehensive search with personalization"""
        if not query.strip():
            return {'success': False, 'error': 'Empty search query'}
        
        try:
            user_profile = self._get_user_profile(user_id)
            
            # Search all categories
            learning_results = self._search_learning_resources(query, user_profile, filters)
            skill_test_results = self._search_skill_tests(query, user_profile, filters)
            job_results = self._search_jobs(query, user_profile, filters)
            
            all_results = {
                'learning_resources': learning_results,
                'skill_tests': skill_test_results,
                'job_openings': job_results,
                'total_count': len(learning_results) + len(skill_test_results) + len(job_results),
                'personalized_recommendations': self._generate_recommendations(query, user_profile),
                'search_metadata': {
                    'query': query,
                    'user_id': user_id,
                    'timestamp': datetime.now().isoformat()
                }
            }
            
            # Log analytics
            self._log_search_analytics(user_id, query, all_results['total_count'])
            
            return {'success': True, 'results': all_results}
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _search_learning_resources(self, query: str, user_profile: Dict, filters: Dict = None) -> List[Dict]:
        """Search learning resources with personalized ranking"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            sql_query = '''
                SELECT id, title, description, content_type, skill_tags, 
                       difficulty_level, duration_minutes, rating, url
                FROM learning_resources
                WHERE (LOWER(title) LIKE ? OR LOWER(description) LIKE ? OR LOWER(skill_tags) LIKE ?)
                ORDER BY rating DESC LIMIT 10
            '''
            
            params = [f'%{query.lower()}%'] * 3
            cursor.execute(sql_query, params)
            results = cursor.fetchall()
            conn.close()
            
            # Format results with personalization
            formatted_results = []
            for row in results:
                resource = {
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'content_type': row[3],
                    'skill_tags': json.loads(row[4]) if row[4] else [],
                    'difficulty_level': row[5],
                    'duration_minutes': row[6],
                    'rating': row[7],
                    'url': row[8],
                    'match_score': self._calculate_learning_match_score(row, query, user_profile),
                    'action_buttons': [
                        {'text': 'Start Learning', 'action': 'start_course', 'primary': True},
                        {'text': 'Save for Later', 'action': 'bookmark', 'primary': False}
                    ]
                }
                formatted_results.append(resource)
            
            # Sort by match score
            formatted_results.sort(key=lambda x: x['match_score'], reverse=True)
            return formatted_results
            
        except Exception as e:
            logger.error(f"Learning resources search error: {e}")
            return []
    
    def _search_skill_tests(self, query: str, user_profile: Dict, filters: Dict = None) -> List[Dict]:
        """Search skill tests with difficulty matching"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            sql_query = '''
                SELECT id, skill_name, test_type, difficulty, estimated_time, description, badge_level
                FROM skill_tests_catalog
                WHERE (LOWER(skill_name) LIKE ? OR LOWER(description) LIKE ?)
                ORDER BY skill_name ASC LIMIT 8
            '''
            
            params = [f'%{query.lower()}%', f'%{query.lower()}%']
            cursor.execute(sql_query, params)
            results = cursor.fetchall()
            conn.close()
            
            formatted_results = []
            for row in results:
                test = {
                    'id': row[0],
                    'skill_name': row[1],
                    'test_type': row[2],
                    'difficulty': row[3],
                    'estimated_time': row[4],
                    'description': row[5],
                    'badge_level': row[6],
                    'match_score': self._calculate_test_match_score(row, query, user_profile),
                    'readiness_level': self._assess_test_readiness(row, user_profile),
                    'action_buttons': [
                        {'text': 'Start Test', 'action': 'start_test', 'primary': True},
                        {'text': 'Check My Fit', 'action': 'assess_readiness', 'primary': False}
                    ]
                }
                formatted_results.append(test)
            
            formatted_results.sort(key=lambda x: x['match_score'], reverse=True)
            return formatted_results
            
        except Exception as e:
            logger.error(f"Skill tests search error: {e}")
            return []
    
    def _search_jobs(self, query: str, user_profile: Dict, filters: Dict = None) -> List[Dict]:
        """Search job openings with match scoring"""
        try:
            # Sample job data for demo
            sample_jobs = [
                {
                    'id': 'job_001',
                    'title': 'Software Developer',
                    'company': 'TechCorp',
                    'location': 'Bangalore',
                    'experience_required': '1-3 years',
                    'skills_required': ['python', 'django', 'sql'],
                    'salary_range': '₹4-8 LPA',
                    'company_tier': 'tier_2'
                },
                {
                    'id': 'job_002',
                    'title': 'Data Analyst',
                    'company': 'DataFlow Inc',
                    'location': 'Mumbai',
                    'experience_required': '0-2 years',
                    'skills_required': ['sql', 'python', 'data analysis'],
                    'salary_range': '₹3-6 LPA',
                    'company_tier': 'tier_2'
                },
                {
                    'id': 'job_003',
                    'title': 'Frontend Developer',
                    'company': 'WebSolutions',
                    'location': 'Hyderabad',
                    'experience_required': '1-2 years',
                    'skills_required': ['react', 'javascript', 'html'],
                    'salary_range': '₹5-9 LPA',
                    'company_tier': 'tier_3'
                }
            ]
            
            # Filter jobs based on query
            query_lower = query.lower()
            matching_jobs = []
            
            for job in sample_jobs:
                if (query_lower in job['title'].lower() or 
                    query_lower in job['company'].lower() or
                    any(query_lower in skill.lower() for skill in job['skills_required'])):
                    
                    job['match_score'] = self._calculate_job_match_score(job, query, user_profile)
                    job['fit_analysis'] = self._analyze_job_fit(job, user_profile)
                    job['action_buttons'] = [
                        {'text': 'Check My Fit', 'action': 'analyze_fit', 'primary': True},
                        {'text': 'Apply Now', 'action': 'apply_job', 'primary': True}
                    ]
                    matching_jobs.append(job)
            
            matching_jobs.sort(key=lambda x: x['match_score'], reverse=True)
            return matching_jobs[:6]
            
        except Exception as e:
            logger.error(f"Job search error: {e}")
            return []
    
    def _get_user_profile(self, user_id: int) -> Dict[str, Any]:
        """Get user profile for personalization"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT skills, experience_level, preferred_domains
                FROM student_profiles WHERE user_id = ?
            ''', (user_id,))
            
            profile_data = cursor.fetchone()
            conn.close()
            
            if profile_data:
                return {
                    'skills': json.loads(profile_data[0]) if profile_data[0] else [],
                    'experience_level': profile_data[1] or 'beginner',
                    'preferred_domains': json.loads(profile_data[2]) if profile_data[2] else []
                }
            else:
                return {
                    'skills': [],
                    'experience_level': 'beginner',
                    'preferred_domains': []
                }
                
        except Exception as e:
            logger.error(f"Profile retrieval error: {e}")
            return {}
    
    def _calculate_learning_match_score(self, resource_row: tuple, query: str, user_profile: Dict) -> float:
        """Calculate learning resource match score"""
        try:
            title, description, skill_tags = resource_row[1], resource_row[2], resource_row[4]
            skills = json.loads(skill_tags) if skill_tags else []
            
            score = 0.0
            
            # Query match
            combined_text = f"{title} {description}".lower()
            if query.lower() in combined_text:
                score += 0.5
            
            # Skill overlap
            user_skills = [skill.lower() for skill in user_profile.get('skills', [])]
            resource_skills = [skill.lower() for skill in skills]
            
            overlap = len(set(user_skills) & set(resource_skills))
            if resource_skills:
                score += 0.3 * (overlap / len(resource_skills))
            
            # Difficulty matching
            difficulty = resource_row[5]
            user_level = user_profile.get('experience_level', 'beginner')
            if difficulty == user_level:
                score += 0.2
            
            return min(score, 1.0)
            
        except Exception as e:
            return 0.0
    
    def _calculate_test_match_score(self, test_row: tuple, query: str, user_profile: Dict) -> float:
        """Calculate test relevance score"""
        try:
            skill_name = test_row[1].lower()
            score = 0.0
            
            if query.lower() in skill_name:
                score += 0.6
            
            user_skills = [skill.lower() for skill in user_profile.get('skills', [])]
            if skill_name in user_skills:
                score += 0.4
            
            return min(score, 1.0)
            
        except Exception as e:
            return 0.0
    
    def _calculate_job_match_score(self, job: Dict, query: str, user_profile: Dict) -> float:
        """Calculate job match score"""
        try:
            job_skills = set(skill.lower() for skill in job['skills_required'])
            user_skills = set(skill.lower() for skill in user_profile.get('skills', []))
            
            # Skill matching
            overlap = len(job_skills & user_skills)
            skill_score = overlap / len(job_skills) if job_skills else 0
            
            # Query relevance
            query_score = 0.2 if query.lower() in job['title'].lower() else 0
            
            return min(skill_score * 0.8 + query_score, 1.0)
            
        except Exception as e:
            return 0.0
    
    def _analyze_job_fit(self, job: Dict, user_profile: Dict) -> Dict[str, Any]:
        """Analyze job fit percentage"""
        try:
            job_skills = set(skill.lower() for skill in job['skills_required'])
            user_skills = set(skill.lower() for skill in user_profile.get('skills', []))
            
            matching = job_skills & user_skills
            missing = job_skills - user_skills
            
            fit_percentage = len(matching) / len(job_skills) * 100 if job_skills else 0
            
            if fit_percentage >= 80:
                fit_level = "Excellent Fit"
            elif fit_percentage >= 60:
                fit_level = "Good Fit"
            elif fit_percentage >= 40:
                fit_level = "Moderate Fit"
            else:
                fit_level = "Low Fit"
            
            return {
                'fit_percentage': round(fit_percentage, 1),
                'fit_level': fit_level,
                'matching_skills': list(matching),
                'missing_skills': list(missing)
            }
            
        except Exception as e:
            return {'fit_percentage': 0, 'fit_level': 'Unknown'}
    
    def _assess_test_readiness(self, test_row: tuple, user_profile: Dict) -> str:
        """Assess if user is ready for the test"""
        try:
            skill_name = test_row[1].lower()
            difficulty = test_row[3]
            
            user_skills = [skill.lower() for skill in user_profile.get('skills', [])]
            user_level = user_profile.get('experience_level', 'beginner')
            
            if skill_name in user_skills and difficulty == user_level:
                return "Ready"
            elif skill_name in user_skills:
                return "Partial"
            else:
                return "Not Ready"
                
        except Exception as e:
            return "Unknown"
    
    def _generate_recommendations(self, query: str, user_profile: Dict) -> List[Dict[str, str]]:
        """Generate personalized recommendations"""
        try:
            recommendations = []
            
            # Skills to verify
            user_skills = user_profile.get('skills', [])
            if user_skills and len(user_skills) > 0:
                skill = user_skills[0]
                recommendations.append({
                    'type': 'skill_verification',
                    'title': f'Verify Your {skill.title()} Skills',
                    'description': f'Get certified in {skill} to boost your profile',
                    'action': f'verify_{skill.lower()}'
                })
            
            # Learning path suggestion
            if query.lower() in ['python', 'java', 'sql', 'react']:
                recommendations.append({
                    'type': 'learning_path',
                    'title': f'Complete {query.title()} Learning Path',
                    'description': f'Follow our structured {query} curriculum',
                    'action': f'start_path_{query.lower()}'
                })
            
            # Job readiness
            experience_level = user_profile.get('experience_level', 'beginner')
            if experience_level == 'intermediate':
                recommendations.append({
                    'type': 'job_readiness',
                    'title': 'Check Your Job Readiness',
                    'description': 'Take our comprehensive assessment to see how job-ready you are',
                    'action': 'job_readiness_test'
                })
            
            return recommendations[:3]  # Return top 3
            
        except Exception as e:
            logger.error(f"Recommendations error: {e}")
            return []
    
    def _log_search_analytics(self, user_id: int, query: str, result_count: int):
        """Log search for analytics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO search_analytics (user_id, search_query, results_count)
                VALUES (?, ?, ?)
            ''', (user_id, query, result_count))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Analytics logging error: {e}")

# Example usage
if __name__ == "__main__":
    search_engine = SmartSearchEngine()
    
    # Test search
    result = search_engine.search_all("python", user_id=1)
    print(f"Search Results: {result}")