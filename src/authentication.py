"""
Advanced Authentication System for Placement Prediction Platform
Comprehensive user authentication with Flask-Login integration
"""

from flask import Flask, request, session, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from functools import wraps
from src.database import db_manager
from typing import Dict, Optional
import secrets

class User(UserMixin):
    """User class for Flask-Login"""
    
    def __init__(self, user_data: Dict):
        self.id = str(user_data['id'])
        self.first_name = user_data['first_name']
        self.last_name = user_data['last_name']
        self.user_type = user_data['user_type']
        self.email = user_data.get('email', '')
        
    def get_id(self):
        return self.id
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_admin(self):
        return self.user_type == 'admin'
    
    @property
    def is_student(self):
        return self.user_type == 'student'

class AuthenticationManager:
    """
    Comprehensive authentication management system
    """
    
    def __init__(self, app: Flask):
        self.app = app
        self.login_manager = LoginManager()
        self.login_manager.init_app(app)
        self.login_manager.login_view = 'auth.login'
        self.login_manager.login_message = 'Please log in to access this page.'
        self.login_manager.login_message_category = 'info'
        
        # User loader callback
        @self.login_manager.user_loader
        def load_user(user_id):
            return self.get_user_by_id(user_id)
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Load user by ID for Flask-Login"""
        try:
            profile = db_manager.get_student_profile(int(user_id))
            if profile:
                return User(profile)
            return None
        except Exception as e:
            print(f"Error loading user: {e}")
            return None
    
    def register_user(self, form_data: Dict) -> Dict:
        """Register new user with validation"""
        try:
            # Validate required fields
            required_fields = ['email', 'password', 'first_name', 'last_name', 'student_id', 'branch']
            for field in required_fields:
                if not form_data.get(field):
                    return {'success': False, 'message': f'{field.replace("_", " ").title()} is required'}
            
            # Validate email format
            email = form_data['email'].strip().lower()
            if '@' not in email or '.' not in email:
                return {'success': False, 'message': 'Invalid email format'}
            
            # Validate password strength
            password = form_data['password']
            if len(password) < 6:
                return {'success': False, 'message': 'Password must be at least 6 characters long'}
            
            # Create user
            result = db_manager.create_user(
                email=email,
                password=password,
                first_name=form_data['first_name'].strip(),
                last_name=form_data['last_name'].strip(),
                user_type='student',
                student_id=form_data['student_id'].strip(),
                branch=form_data['branch'].strip(),
                academic_year=form_data.get('academic_year', 2024)
            )
            
            return result
            
        except Exception as e:
            return {'success': False, 'message': f'Registration error: {str(e)}'}
    
    def login_user_account(self, email: str, password: str, remember_me: bool = False) -> Dict:
        """Authenticate and login user"""
        try:
            # Authenticate user
            auth_result = db_manager.authenticate_user(email.strip().lower(), password)
            
            if not auth_result['success']:
                return auth_result
            
            # Get full user profile
            user_data = auth_result['user']
            profile = db_manager.get_student_profile(user_data['id'])
            
            if not profile:
                return {'success': False, 'message': 'User profile not found'}
            
            # Create user object and login
            user = User(profile)
            login_user(user, remember=remember_me)
            
            return {
                'success': True,
                'message': 'Login successful',
                'user': user,
                'redirect_url': self._get_redirect_url(user.user_type)
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Login error: {str(e)}'}
    
    def _get_redirect_url(self, user_type: str) -> str:
        """Get appropriate redirect URL based on user type"""
        if user_type == 'admin':
            return url_for('admin_dashboard')
        else:
            return url_for('student_dashboard')
    
    def logout_user_account(self):
        """Logout current user"""
        logout_user()
        flash('You have been logged out successfully.', 'success')
        return redirect(url_for('auth.login'))

def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    """Decorator to require student access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_student:
            flash('Student access required.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Initialize authentication manager (will be setup in main app)
auth_manager = None

def init_auth(app: Flask):
    """Initialize authentication system"""
    global auth_manager
    app.secret_key = secrets.token_hex(32)  # Generate secure secret key
    auth_manager = AuthenticationManager(app)
    return auth_manager