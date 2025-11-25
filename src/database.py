"""
Industry-Ready Database Management System
Comprehensive database schema for user management, assessments, and analytics
"""

import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json
import pandas as pd
from contextlib import contextmanager

class DatabaseManager:
    """
    Comprehensive database management for the placement prediction system
    """
    
    def __init__(self, db_path: str = "data/placement_system.db"):
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Database connection context manager"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize all database tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table - comprehensive user management
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    user_type TEXT DEFAULT 'student',
                    student_id TEXT UNIQUE,
                    branch TEXT,
                    academic_year INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    email_verified BOOLEAN DEFAULT 0
                )
            ''')
            
            # Student profiles - detailed academic information
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS student_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE,
                    cgpa REAL,
                    tenth_percentage REAL,
                    twelfth_percentage REAL,
                    num_projects INTEGER DEFAULT 0,
                    num_internships INTEGER DEFAULT 0,
                    num_certifications INTEGER DEFAULT 0,
                    programming_languages TEXT,
                    leetcode_score INTEGER DEFAULT 0,
                    codechef_rating INTEGER DEFAULT 0,
                    communication_score REAL DEFAULT 0,
                    leadership_score REAL DEFAULT 0,
                    num_hackathons INTEGER DEFAULT 0,
                    club_participation INTEGER DEFAULT 0,
                    online_courses INTEGER DEFAULT 0,
                    current_placement_status TEXT DEFAULT 'not_placed',
                    target_companies TEXT,
                    preferred_locations TEXT,
                    expected_salary REAL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            ''')
            
            # Assessment results - skill assessment tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS assessment_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    assessment_type TEXT NOT NULL,
                    language TEXT,
                    level TEXT,
                    score INTEGER,
                    total_questions INTEGER,
                    percentage REAL,
                    time_taken INTEGER,
                    assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    detailed_results TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            ''')
            
            # Placement predictions - prediction history
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS placement_predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    prediction_probability REAL,
                    model_used TEXT,
                    feature_importance TEXT,
                    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    profile_snapshot TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            ''')
            
            # Course progress - learning path tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS course_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    course_title TEXT,
                    course_platform TEXT,
                    status TEXT DEFAULT 'not_started',
                    progress_percentage REAL DEFAULT 0,
                    started_date TIMESTAMP,
                    completed_date TIMESTAMP,
                    estimated_completion TIMESTAMP,
                    priority INTEGER DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            ''')
            
            # Sessions - user session management
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    session_token TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    ip_address TEXT,
                    user_agent TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            ''')
            
            # Admin logs - system activity tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS admin_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    admin_id INTEGER,
                    action TEXT,
                    target_table TEXT,
                    target_id INTEGER,
                    details TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (admin_id) REFERENCES users (id)
                )
            ''')
            
            # System settings - configurable parameters
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    setting_key TEXT UNIQUE,
                    setting_value TEXT,
                    description TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_by INTEGER,
                    FOREIGN KEY (updated_by) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
            print("✅ Database initialized successfully!")
    
    def hash_password(self, password: str) -> Tuple[str, str]:
        """Generate secure password hash with salt"""
        salt = secrets.token_hex(32)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return password_hash.hex(), salt
    
    def verify_password(self, password: str, password_hash: str, salt: str) -> bool:
        """Verify password against stored hash"""
        test_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return test_hash.hex() == password_hash
    
    def create_user(self, email: str, password: str, first_name: str, last_name: str, 
                   user_type: str = 'student', **kwargs) -> Dict:
        """Create new user account"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if user already exists
                cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
                if cursor.fetchone():
                    return {'success': False, 'message': 'Email already registered'}
                
                # Hash password
                password_hash, salt = self.hash_password(password)
                
                # Insert user
                cursor.execute('''
                    INSERT INTO users 
                    (email, password_hash, salt, first_name, last_name, user_type, student_id, branch, academic_year)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (email, password_hash, salt, first_name, last_name, user_type,
                      kwargs.get('student_id'), kwargs.get('branch'), kwargs.get('academic_year')))
                
                user_id = cursor.lastrowid
                
                # Create student profile if user is a student
                if user_type == 'student':
                    cursor.execute('''
                        INSERT INTO student_profiles (user_id) VALUES (?)
                    ''', (user_id,))
                
                conn.commit()
                
                return {
                    'success': True, 
                    'message': 'User created successfully',
                    'user_id': user_id
                }
                
        except Exception as e:
            return {'success': False, 'message': f'Error creating user: {str(e)}'}
    
    def authenticate_user(self, email: str, password: str) -> Dict:
        """Authenticate user login"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT id, password_hash, salt, first_name, last_name, user_type, is_active
                    FROM users WHERE email = ?
                ''', (email,))
                
                user = cursor.fetchone()
                if not user:
                    return {'success': False, 'message': 'Invalid email or password'}
                
                if not user['is_active']:
                    return {'success': False, 'message': 'Account is deactivated'}
                
                if not self.verify_password(password, user['password_hash'], user['salt']):
                    return {'success': False, 'message': 'Invalid email or password'}
                
                # Update last login
                cursor.execute('UPDATE users SET last_login = ? WHERE id = ?', 
                             (datetime.now(), user['id']))
                conn.commit()
                
                return {
                    'success': True,
                    'message': 'Login successful',
                    'user': {
                        'id': user['id'],
                        'first_name': user['first_name'],
                        'last_name': user['last_name'],
                        'user_type': user['user_type']
                    }
                }
                
        except Exception as e:
            return {'success': False, 'message': f'Authentication error: {str(e)}'}
    
    def create_session(self, user_id: int, ip_address: str = None, user_agent: str = None) -> str:
        """Create user session"""
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=24)
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO user_sessions 
                    (user_id, session_token, expires_at, ip_address, user_agent)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user_id, session_token, expires_at, ip_address, user_agent))
                conn.commit()
                
            return session_token
        except Exception as e:
            print(f"Error creating session: {e}")
            return None
    
    def validate_session(self, session_token: str) -> Dict:
        """Validate user session"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT s.user_id, u.first_name, u.last_name, u.user_type
                    FROM user_sessions s
                    JOIN users u ON s.user_id = u.id
                    WHERE s.session_token = ? AND s.expires_at > ? AND s.is_active = 1
                ''', (session_token, datetime.now()))
                
                session = cursor.fetchone()
                if session:
                    return {
                        'valid': True,
                        'user': {
                            'id': session['user_id'],
                            'first_name': session['first_name'],
                            'last_name': session['last_name'],
                            'user_type': session['user_type']
                        }
                    }
                
                return {'valid': False}
                
        except Exception as e:
            print(f"Session validation error: {e}")
            return {'valid': False}
    
    def update_student_profile(self, user_id: int, profile_data: Dict) -> bool:
        """Update student academic profile"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Build update query dynamically
                fields = []
                values = []
                for key, value in profile_data.items():
                    if key in ['cgpa', 'tenth_percentage', 'twelfth_percentage', 'num_projects',
                              'num_internships', 'num_certifications', 'programming_languages',
                              'leetcode_score', 'codechef_rating', 'communication_score',
                              'leadership_score', 'num_hackathons', 'club_participation',
                              'online_courses', 'target_companies', 'preferred_locations', 'expected_salary']:
                        fields.append(f"{key} = ?")
                        values.append(value)
                
                if not fields:
                    return False
                
                fields.append("updated_at = ?")
                values.append(datetime.now())
                values.append(user_id)
                
                query = f"UPDATE student_profiles SET {', '.join(fields)} WHERE user_id = ?"
                cursor.execute(query, values)
                conn.commit()
                
                return cursor.rowcount > 0
                
        except Exception as e:
            print(f"Error updating profile: {e}")
            return False
    
    def get_student_profile(self, user_id: int) -> Dict:
        """Get complete student profile"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT u.*, sp.*
                    FROM users u
                    LEFT JOIN student_profiles sp ON u.id = sp.user_id
                    WHERE u.id = ?
                ''', (user_id,))
                
                profile = cursor.fetchone()
                if profile:
                    return dict(profile)
                return {}
                
        except Exception as e:
            print(f"Error getting profile: {e}")
            return {}
    
    def save_assessment_result(self, user_id: int, assessment_data: Dict) -> bool:
        """Save skill assessment results"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO assessment_results 
                    (user_id, assessment_type, language, level, score, total_questions, 
                     percentage, time_taken, detailed_results)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id,
                    assessment_data.get('assessment_type', 'skill_quiz'),
                    assessment_data.get('language'),
                    assessment_data.get('level'),
                    assessment_data.get('score'),
                    assessment_data.get('total_questions'),
                    assessment_data.get('percentage'),
                    assessment_data.get('time_taken'),
                    json.dumps(assessment_data.get('detailed_results', {}))
                ))
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Error saving assessment: {e}")
            return False
    
    def save_placement_prediction(self, user_id: int, prediction_data: Dict) -> bool:
        """Save placement prediction results"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO placement_predictions 
                    (user_id, prediction_probability, model_used, feature_importance, profile_snapshot)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    user_id,
                    prediction_data.get('probability'),
                    prediction_data.get('model_used'),
                    json.dumps(prediction_data.get('feature_importance', {})),
                    json.dumps(prediction_data.get('profile_snapshot', {}))
                ))
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Error saving prediction: {e}")
            return False
    
    def get_dashboard_analytics(self) -> Dict:
        """Get analytics data for dashboard"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Total users
                cursor.execute("SELECT COUNT(*) as total FROM users WHERE user_type = 'student'")
                total_students = cursor.fetchone()['total']
                
                # Recent assessments
                cursor.execute("""
                    SELECT COUNT(*) as recent_assessments 
                    FROM assessment_results 
                    WHERE assessment_date > datetime('now', '-7 days')
                """)
                recent_assessments = cursor.fetchone()['recent_assessments']
                
                # Average placement probability
                cursor.execute("""
                    SELECT AVG(prediction_probability) as avg_probability
                    FROM placement_predictions
                    WHERE prediction_date > datetime('now', '-30 days')
                """)
                avg_prob_result = cursor.fetchone()
                avg_probability = avg_prob_result['avg_probability'] if avg_prob_result['avg_probability'] else 0
                
                # Branch distribution
                cursor.execute("""
                    SELECT branch, COUNT(*) as count
                    FROM users 
                    WHERE user_type = 'student' AND branch IS NOT NULL
                    GROUP BY branch
                """)
                branch_distribution = [dict(row) for row in cursor.fetchall()]
                
                return {
                    'total_students': total_students,
                    'recent_assessments': recent_assessments,
                    'average_placement_probability': float(avg_probability) if avg_probability else 0,
                    'branch_distribution': branch_distribution
                }
                
        except Exception as e:
            print(f"Error getting analytics: {e}")
            return {}
    
    def get_all_students(self) -> List[Dict]:
        """Get all students with basic profile information"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # First check if there are any users at all
                cursor.execute("SELECT COUNT(*) as total FROM users WHERE user_type = 'student'")
                total_count = cursor.fetchone()['total']
                print(f"Debug: Found {total_count} students in database")
                
                if total_count == 0:
                    print("Debug: No students found in database")
                    return []
                
                cursor.execute('''
                    SELECT u.id, u.first_name, u.last_name, u.email, u.branch, u.academic_year,
                           u.created_at, sp.cgpa, sp.tenth_percentage, sp.twelfth_percentage,
                           sp.num_projects, sp.num_internships, sp.programming_languages,
                           0 as total_assessments,
                           0 as avg_score,
                           0 as prediction_probability
                    FROM users u
                    LEFT JOIN student_profiles sp ON u.id = sp.user_id
                    WHERE u.user_type = 'student'
                    ORDER BY u.created_at DESC
                ''')
                
                students = [dict(row) for row in cursor.fetchall()]
                print(f"Debug: Retrieved {len(students)} student records")
                return students
                
        except Exception as e:
            print(f"Error getting all students: {e}")
            return []
    
    def get_student_assessments(self, user_id: int) -> List[Dict]:
        """Get all assessments for a student"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM assessment_results 
                    WHERE user_id = ? 
                    ORDER BY assessment_date DESC
                ''', (user_id,))
                return [dict(row) for row in cursor.fetchall()]
                
        except Exception as e:
            print(f"Error getting student assessments: {e}")
            return []
    
    def get_student_predictions(self, user_id: int) -> List[Dict]:
        """Get all predictions for a student"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM placement_predictions 
                    WHERE user_id = ? 
                    ORDER BY prediction_date DESC
                ''', (user_id,))
                return [dict(row) for row in cursor.fetchall()]
                
        except Exception as e:
            print(f"Error getting student predictions: {e}")
            return []
    
    def get_student_analytics(self, user_id: int) -> Dict:
        """Get comprehensive analytics for a specific student"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get assessment results
                cursor.execute("""
                    SELECT assessment_type, score, percentage, assessment_date, language
                    FROM assessment_results 
                    WHERE user_id = ? 
                    ORDER BY assessment_date DESC
                """, (user_id,))
                assessments = [dict(row) for row in cursor.fetchall()]
                
                # Get placement prediction history
                cursor.execute("""
                    SELECT prediction_probability, model_used, prediction_date
                    FROM placement_predictions 
                    WHERE user_id = ? 
                    ORDER BY prediction_date DESC
                    LIMIT 10
                """, (user_id,))
                predictions = [dict(row) for row in cursor.fetchall()]
                
                # Calculate performance statistics
                assessment_stats = {
                    'total_assessments': len(assessments),
                    'average_score': 0,
                    'by_type': {},
                    'recent_activity': [],
                    'skill_distribution': {}
                }
                
                if assessments:
                    # Calculate average score
                    valid_scores = [a['percentage'] for a in assessments if a['percentage'] is not None]
                    if valid_scores:
                        assessment_stats['average_score'] = sum(valid_scores) / len(valid_scores)
                    
                    # Group by assessment type
                    for assessment in assessments:
                        atype = assessment['assessment_type']
                        if atype not in assessment_stats['by_type']:
                            assessment_stats['by_type'][atype] = []
                        assessment_stats['by_type'][atype].append(assessment)
                    
                    # Recent activity (last 30 days)
                    from datetime import datetime, timedelta
                    thirty_days_ago = datetime.now() - timedelta(days=30)
                    assessment_stats['recent_activity'] = [
                        a for a in assessments 
                        if datetime.fromisoformat(a['assessment_date'].replace('Z', '+00:00')) > thirty_days_ago
                    ][:5]
                    
                    # Skills distribution
                    for assessment in assessments:
                        if assessment['language']:
                            lang = assessment['language']
                            if lang not in assessment_stats['skill_distribution']:
                                assessment_stats['skill_distribution'][lang] = []
                            assessment_stats['skill_distribution'][lang].append(assessment['percentage'])
                
                # Calculate placement prediction stats
                prediction_stats = {
                    'current_probability': 0,
                    'trend': 'stable',
                    'history': predictions[:5],
                    'improvement_over_time': 0
                }
                
                if predictions:
                    prediction_stats['current_probability'] = predictions[0]['prediction_probability']
                    if len(predictions) > 1:
                        old_prob = predictions[-1]['prediction_probability']
                        new_prob = predictions[0]['prediction_probability']
                        improvement = ((new_prob - old_prob) / old_prob) * 100 if old_prob > 0 else 0
                        prediction_stats['improvement_over_time'] = improvement
                        
                        if improvement > 5:
                            prediction_stats['trend'] = 'improving'
                        elif improvement < -5:
                            prediction_stats['trend'] = 'declining'
                
                return {
                    'assessments': assessment_stats,
                    'predictions': prediction_stats,
                    'profile_completion': self._calculate_profile_completion(user_id)
                }
                
        except Exception as e:
            print(f"Error getting student analytics: {e}")
            return {
                'assessments': {'total_assessments': 0, 'average_score': 0, 'by_type': {}, 'recent_activity': [], 'skill_distribution': {}},
                'predictions': {'current_probability': 0, 'trend': 'stable', 'history': [], 'improvement_over_time': 0},
                'profile_completion': 0
            }
    
    def _calculate_profile_completion(self, user_id: int) -> int:
        """Calculate profile completion percentage"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
                profile = cursor.fetchone()
                
                if not profile:
                    return 0
                
                # Convert Row to dict for easier access
                profile_dict = dict(profile)
                
                required_fields = ['cgpa', 'tenth_percentage', 'twelfth_percentage', 'num_projects', 
                                 'num_internships', 'programming_languages', 'leetcode_score']
                
                completed = 0
                for field in required_fields:
                    if profile_dict.get(field) and profile_dict[field] not in [None, '', 0]:
                        completed += 1
                
                return int((completed / len(required_fields)) * 100)
                
        except Exception as e:
            print(f"Error calculating profile completion: {e}")
            return 0

# Initialize database on import
db_manager = DatabaseManager()