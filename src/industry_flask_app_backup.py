"""
Industry-Ready Placement Prediction System
Comprehensive Flask application with authentication, dashboard, and deep learning
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, Blueprint
from flask_login import login_required, current_user, logout_user
import sys
import os
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from werkzeug.security import check_password_hash, generate_password_hash

# Add utils to path
sys.path.append('utils')

# Import all components
from src.database import db_manager
from src.authentication import init_auth, admin_required, student_required, auth_manager
from src.model_training import PlacementPredictor
from deep_learning_model import DeepPlacementPredictor
from skill_assessment import SkillAssessmentEngine
from course_recommendation_engine import CourseRecommendationEngine
from recommendations import PlacementRecommendationEngine

# Import our new JSON utility
from utils.json_utils import safe_jsonify

# Import new assessment modules
from comprehensive_assessment import ComprehensiveAssessmentEngine
from communication_assessment import CommunicationAssessmentEngine
from situational_judgment_test import SituationalJudgmentEngine
from resume_scorer import ResumeScorer
from mock_interview_simulator import MockInterviewSimulator

# Import Trust but Verify modules
from skill_verification_engine import SkillVerificationEngine
from live_coding_engine import LiveCodingChallengeManager
from sql_sandbox_engine import SQLSandboxEngine
from framework_code_review_engine import FrameworkCodeReviewEngine
from verified_skill_badge_system import VerifiedSkillBadgeSystem
from light_proctoring_system import LightProctoringSystem

# Import Career Guidance modules
from ats_resume_analyzer import ATSResumeAnalyzer
from conversational_ai_chatbot import ConversationalAIChatbot
from smart_search_engine import SmartSearchEngine
from company_role_prediction import CompanyRolePredictionEngine

# Initialize Flask app
app = Flask(__name__, template_folder='templates')

# Initialize authentication system
auth_manager = init_auth(app)

# Initialize ML components
print("🚀 Initializing ML Components...")
predictor = PlacementPredictor()

# Try to initialize deep learning model (optional)
try:
    from deep_learning_model import DeepPlacementPredictor
    deep_predictor = DeepPlacementPredictor()
    USE_DEEP_MODEL = True
    print("✓ Deep learning model available")
except ImportError as e:
    print(f"⚠️ Deep learning model not available: {e}")
    print("⚠️ Using traditional ML models only")
    deep_predictor = None
    USE_DEEP_MODEL = False
skill_engine = SkillAssessmentEngine()
course_engine = CourseRecommendationEngine()
recommendation_engine = PlacementRecommendationEngine()

# Initialize new assessment engines
comprehensive_engine = ComprehensiveAssessmentEngine()
communication_engine = CommunicationAssessmentEngine()
sjt_engine = SituationalJudgmentEngine()
resume_scorer = ResumeScorer()
interview_simulator = MockInterviewSimulator()

# Initialize Trust but Verify engines
verification_engine = SkillVerificationEngine()
live_coding_manager = LiveCodingChallengeManager()
sql_sandbox = SQLSandboxEngine()
framework_engine = FrameworkCodeReviewEngine()
badge_system = VerifiedSkillBadgeSystem()
proctoring_system = LightProctoringSystem()

# Initialize Career Guidance engines
ats_analyzer = ATSResumeAnalyzer()
ai_chatbot = ConversationalAIChatbot()
smart_search = SmartSearchEngine()
company_predictor = CompanyRolePredictionEngine()

# Load models on startup
print("📦 Loading trained models...")
predictor.load_models()

if USE_DEEP_MODEL and deep_predictor:
    try:
        deep_predictor.load_model()
        print("✅ Deep learning model loaded successfully")
    except Exception as e:
        print(f"⚠️ Deep learning model failed to load: {e}")
        print("⚠️ Falling back to traditional ML models")
        USE_DEEP_MODEL = False
else:
    print("⚠️ Using traditional ML models only")

# Create authentication blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me') == 'on'
        
        if not email or not password:
            flash('Please fill in all fields.', 'error')
            return render_template('auth/login.html')
        
        # Authenticate user
        result = auth_manager.login_user_account(email, password, remember_me)
        
        if result['success']:
            flash(f"Welcome back, {result['user'].first_name}!", 'success')
            return redirect(result['redirect_url'])
        else:
            flash(result['message'], 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if request.method == 'POST':
        form_data = {
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'confirm_password': request.form.get('confirm_password'),
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'student_id': request.form.get('student_id'),
            'branch': request.form.get('branch'),
            'academic_year': request.form.get('academic_year', 2024)
        }
        
        # Validate password confirmation
        if form_data['password'] != form_data['confirm_password']:
            flash('Passwords do not match.', 'error')
            return render_template('auth/register.html')
        
        # Register user
        result = auth_manager.register_user(form_data)
        
        if result['success']:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(result['message'], 'error')
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout user"""
    return auth_manager.logout_user_account()

# Register auth blueprint
app.register_blueprint(auth_bp)

# Main routes
@app.route('/')
def index():
    """Home page - redirect based on authentication status"""
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))
    return redirect(url_for('auth.login'))

@app.route('/student-dashboard')
@login_required
@student_required
def student_dashboard():
    """Student dashboard with personalized content"""
    # Get student profile
    profile = db_manager.get_student_profile(int(current_user.id))
    
    # Get recent assessments
    assessments = []  # Will be populated from database
    
    # Get placement prediction history
    predictions = []  # Will be populated from database
    
    # Get course progress
    courses = []  # Will be populated from database
    
    return render_template('student/dashboard.html', 
                         profile=profile, 
                         assessments=assessments,
                         predictions=predictions,
                         courses=courses)

@app.route('/admin-dashboard')
@login_required
@admin_required
def admin_dashboard():
    """Admin dashboard with system analytics"""
    # Get dashboard analytics
    analytics = db_manager.get_dashboard_analytics()
    
    # Get recent activity
    recent_users = []  # Recent registrations
    recent_assessments = []  # Recent skill assessments
    
    return render_template('admin/dashboard.html',
                         analytics=analytics,
                         recent_users=recent_users,
                         recent_assessments=recent_assessments)

@app.route('/profile')
@login_required
@student_required
def profile():
    """Student profile management"""
    profile = db_manager.get_student_profile(int(current_user.id))
    return render_template('student/profile.html', profile=profile)

@app.route('/update-profile', methods=['POST'])
@login_required
@student_required
def update_profile():
    """Update student profile"""
    try:
        profile_data = {
            'cgpa': float(request.form.get('cgpa', 0)),
            'tenth_percentage': float(request.form.get('tenth_percentage', 0)),
            'twelfth_percentage': float(request.form.get('twelfth_percentage', 0)),
            'num_projects': int(request.form.get('num_projects', 0)),
            'num_internships': int(request.form.get('num_internships', 0)),
            'num_certifications': int(request.form.get('num_certifications', 0)),
            'programming_languages': request.form.get('programming_languages', ''),
            'leetcode_score': int(request.form.get('leetcode_score', 0)),
            'codechef_rating': int(request.form.get('codechef_rating', 0)),
            'communication_score': float(request.form.get('communication_score', 0)),
            'leadership_score': float(request.form.get('leadership_score', 0)),
            'num_hackathons': int(request.form.get('num_hackathons', 0)),
            'club_participation': int(request.form.get('club_participation', 0)),
            'online_courses': int(request.form.get('online_courses', 0)),
            'target_companies': request.form.get('target_companies', ''),
            'preferred_locations': request.form.get('preferred_locations', ''),
            'expected_salary': float(request.form.get('expected_salary', 0))
        }
        
        success = db_manager.update_student_profile(int(current_user.id), profile_data)
        
        if success:
            flash('Profile updated successfully!', 'success')
        else:
            flash('Failed to update profile.', 'error')
            
    except Exception as e:
        flash(f'Error updating profile: {str(e)}', 'error')
    
    return redirect(url_for('profile'))

@app.route('/placement-prediction')
@login_required
@student_required
def placement_prediction():
    """Placement prediction page"""
    profile = db_manager.get_student_profile(int(current_user.id))
    return render_template('student/prediction.html', profile=profile)

@app.route('/predict-placement', methods=['POST'])
@login_required
@student_required
def predict_placement():
    """Make placement prediction"""
    try:
        # Get student profile
        profile = db_manager.get_student_profile(int(current_user.id))
        
        if not profile:
            return jsonify({'success': False, 'message': 'Profile not found'})
        
        # Filter profile data to only include ML features (exclude output variables)
        ml_features = {
            'student_id': profile.get('student_id', f'user_{current_user.id}'),
            'branch': profile.get('branch', 'Computer Science'),
            'cgpa': profile.get('cgpa', 0.0),
            'tenth_percentage': profile.get('tenth_percentage', 0.0),
            'twelfth_percentage': profile.get('twelfth_percentage', 0.0),
            'num_projects': profile.get('num_projects', 0),
            'num_internships': profile.get('num_internships', 0),
            'num_certifications': profile.get('num_certifications', 0),
            'programming_languages': profile.get('programming_languages', ''),
            'leetcode_score': profile.get('leetcode_score', 0),
            'codechef_rating': profile.get('codechef_rating', 0),
            'communication_score': profile.get('communication_score', 0.0),
            'leadership_score': profile.get('leadership_score', 0.0),
            'num_hackathons': profile.get('num_hackathons', 0),
            'club_participation': profile.get('club_participation', 0),
            'online_courses': profile.get('online_courses', 0)
            # Note: Removed placed, salary_package, and package_category as these are output variables
        }
        
        # Choose model based on availability
        if USE_DEEP_MODEL and deep_predictor:
            result = deep_predictor.predict(ml_features)
            model_used = 'deep_learning'
        else:
            result = predictor.predict_placement(ml_features)
            model_used = 'random_forest'
        
        if result:
            # Save prediction to database
            prediction_data = {
                'probability': result['probability'],
                'model_used': model_used,
                'feature_importance': predictor.get_feature_importance_for_prediction(ml_features) if not USE_DEEP_MODEL else {},
                'profile_snapshot': ml_features
            }
            
            db_manager.save_placement_prediction(int(current_user.id), prediction_data)
            
            # Get recommendations if probability is low
            recommendations = []
            if result['probability'] < 0.6:
                analysis = recommendation_engine.analyze_student_profile(ml_features)
                recommendations = analysis.get('recommendations', [])[:5]
            
            # Use safe_jsonify to handle any NaN values in the response
            response_data = {
                'success': True,
                'probability': result['probability'],
                'prediction': result.get('prediction', int(result['probability'] > 0.5)),
                'placement_chance': f"{result['probability']*100:.1f}%",
                'confidence': result.get('confidence', result['probability']),
                'model_used': model_used,
                'recommendations': recommendations
            }
            
            return jsonify(safe_jsonify(response_data))
        else:
            return jsonify({'success': False, 'message': 'Prediction failed'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/skill-assessment')
@login_required
@student_required
def skill_assessment():
    """Skill assessment page"""
    return render_template('student/skill_assessment.html')

@app.route('/conduct-assessment', methods=['POST'])
@login_required
@student_required
def conduct_assessment():
    """Conduct skill assessment"""
    try:
        data = request.get_json()
        languages = data.get('languages', '').split(',')
        languages = [lang.strip() for lang in languages if lang.strip()]
        
        if not languages:
            return jsonify({'success': False, 'message': 'Please select at least one language'})
        
        # Conduct assessment
        assessment_results = skill_engine.conduct_skill_assessment(languages, questions_per_level=3)
        skill_report = skill_engine.generate_skill_report(assessment_results)
        
        # Save to database
        for language, result in assessment_results.items():
            assessment_data = {
                'assessment_type': 'skill_quiz',
                'language': language,
                'level': result.get('proficiency_level', 'beginner'),
                'score': result.get('overall_score', 0),
                'total_questions': result.get('total_questions', 0),
                'percentage': result.get('overall_percentage', 0),
                'time_taken': 300,  # 5 minutes estimated
                'detailed_results': result
            }
            db_manager.save_assessment_result(int(current_user.id), assessment_data)
        
        return jsonify({
            'success': True,
            'report': skill_report,
            'detailed_results': assessment_results
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Assessment error: {str(e)}'})

@app.route('/course-recommendations')
@login_required
@student_required
def course_recommendations():
    """Course recommendations page"""
    return render_template('student/courses.html')

@app.route('/get-course-recommendations', methods=['POST'])
@login_required
@student_required
def get_course_recommendations():
    """Get personalized course recommendations"""
    try:
        # Get student profile
        profile = db_manager.get_student_profile(int(current_user.id))
        
        if not profile:
            return jsonify({'success': False, 'message': 'Profile not found'})
        
        # Get target companies from form or profile
        target_companies = request.json.get('target_companies', [])
        if not target_companies and profile.get('target_companies'):
            target_companies = profile['target_companies'].split(',')
        
        # Get course recommendations
        recommendations = course_engine.recommend_courses_for_student(profile, target_companies)
        
        # Format response
        formatted_recommendations = {
            'immediate_priorities': [{
                'title': course.title,
                'platform': course.platform,
                'duration': course.duration,
                'price': course.price,
                'rating': course.rating,
                'url': course.url,
                'description': course.description
            } for course in recommendations['immediate_priorities']],
            'free_alternatives': [{
                'title': course.title,
                'platform': course.platform,
                'duration': course.duration,
                'url': course.url,
                'description': course.description
            } for course in recommendations['free_alternatives'][:5]],
            'company_specific': {
                company: [{
                    'title': course.title,
                    'platform': course.platform,
                    'price': course.price,
                    'url': course.url
                } for course in courses[:3]]
                for company, courses in recommendations.get('company_specific', {}).items()
            }
        }
        
        return jsonify({
            'success': True,
            'recommendations': formatted_recommendations
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Recommendation error: {str(e)}'})

@app.route('/train-models')
@login_required
@admin_required
def train_models():
    """Model training page for admins"""
    return render_template('admin/model_training.html')

@app.route('/trigger-training', methods=['POST'])
@login_required
@admin_required
def trigger_training():
    """Trigger model training"""
    try:
        model_type = request.json.get('model_type', 'traditional')
        
        if model_type == 'deep_learning':
            # Train deep learning model
            if not os.path.exists('data/placement_data.csv'):
                return jsonify({'success': False, 'message': 'Training data not found'})
            
            df = pd.read_csv('data/placement_data.csv')
            metrics = deep_predictor.train_model(df)
            deep_predictor.save_model()
            
            return jsonify({
                'success': True, 
                'message': 'Deep learning model trained successfully',
                'metrics': metrics
            })
        else:
            # Train traditional models
            success = predictor.train_all_models()
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Traditional models trained successfully',
                    'metrics': predictor.model_scores
                })
            else:
                return jsonify({'success': False, 'message': 'Training failed'})
                
    except Exception as e:
        return jsonify({'success': False, 'message': f'Training error: {str(e)}')

@app.route('/system-analytics')
@login_required
@admin_required
def system_analytics():
    """System analytics and reports"""
    analytics = db_manager.get_dashboard_analytics()
    return render_template('admin/analytics.html', analytics=analytics)

# ===== NEW ADVANCED ASSESSMENT ROUTES =====

@app.route('/assessment-hub')
@login_required
@student_required
def assessment_hub():
    """Assessment hub with all available assessments"""
    return render_template('student/assessment_hub.html')

@app.route('/comprehensive-assessment')
@login_required
@student_required
def comprehensive_assessment():
    """Comprehensive aptitude and cognitive assessment"""
    return render_template('student/comprehensive_assessment.html')

@app.route('/start-comprehensive-assessment', methods=['POST'])
@login_required
@student_required
def start_comprehensive_assessment():
    """Start comprehensive assessment"""
    try:
        data = request.get_json()
        test_type = data.get('test_type', 'balanced')  # balanced, logical_reasoning, quantitative, etc.
        difficulty = data.get('difficulty', 'adaptive')
        
        # Generate test configuration
        test_config = comprehensive_engine.generate_test_config(
            test_type=test_type,
            difficulty_level=difficulty,
            num_questions=20
        )
        
        return jsonify({
            'success': True,
            'test_config': test_config,
            'session_id': f"comprehensive_{current_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error starting assessment: {str(e)}'})

@app.route('/submit-comprehensive-assessment', methods=['POST'])
@login_required
@student_required
def submit_comprehensive_assessment():
    """Submit comprehensive assessment responses"""
    try:
        data = request.get_json()
        test_config = data.get('test_config')
        user_responses = data.get('responses')
        
        # Evaluate responses
        evaluation = comprehensive_engine.evaluate_test_performance(test_config, user_responses)
        
        # Save to database
        assessment_data = {
            'assessment_type': 'comprehensive_aptitude',
            'test_config': test_config,
            'user_responses': user_responses,
            'evaluation_results': evaluation,
            'ml_features': evaluation.get('ml_features', {})
        }
        db_manager.save_assessment_result(int(current_user.id), assessment_data)
        
        return jsonify({
            'success': True,
            'evaluation': evaluation
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error evaluating assessment: {str(e)}'})

@app.route('/communication-assessment')
@login_required
@student_required
def communication_assessment():
    """Written communication assessment"""
    return render_template('student/communication_assessment.html')

@app.route('/start-communication-test', methods=['POST'])
@login_required
@student_required
def start_communication_test():
    """Start communication assessment"""
    try:
        data = request.get_json()
        prompt_type = data.get('prompt_type', 'email')
        
        # Generate prompt configuration
        prompt_config = communication_engine.generate_writing_prompt(prompt_type)
        
        return jsonify({
            'success': True,
            'prompt_config': prompt_config,
            'session_id': f"communication_{current_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error starting communication test: {str(e)}'})

@app.route('/submit-communication-response', methods=['POST'])
@login_required
@student_required
def submit_communication_response():
    """Submit written communication response"""
    try:
        data = request.get_json()
        prompt_config = data.get('prompt_config')
        user_response = data.get('response')
        time_taken = data.get('time_taken', 0)
        
        # Evaluate response
        evaluation = communication_engine.evaluate_written_response(
            prompt_config, user_response, time_taken
        )
        
        # Save to database
        assessment_data = {
            'assessment_type': 'written_communication',
            'prompt_config': prompt_config,
            'user_response': user_response,
            'evaluation_results': evaluation,
            'time_taken': time_taken
        }
        db_manager.save_assessment_result(int(current_user.id), assessment_data)
        
        return jsonify({
            'success': True,
            'evaluation': evaluation
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error evaluating communication: {str(e)}'})

@app.route('/situational-judgment-test')
@login_required
@student_required
def situational_judgment_test():
    """Situational Judgment Test for behavioral assessment"""
    return render_template('student/sjt_assessment.html')

@app.route('/start-sjt-assessment', methods=['POST'])
@login_required
@student_required
def start_sjt_assessment():
    """Start SJT assessment"""
    try:
        data = request.get_json()
        focus_area = data.get('focus_area', 'general')  # leadership, teamwork, problem_solving, etc.
        
        # Generate SJT configuration
        assessment_config = sjt_engine.generate_sjt_assessment(focus_area)
        
        return jsonify({
            'success': True,
            'assessment_config': assessment_config,
            'session_id': f"sjt_{current_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error starting SJT assessment: {str(e)}'})

@app.route('/submit-sjt-responses', methods=['POST'])
@login_required
@student_required
def submit_sjt_responses():
    """Submit SJT assessment responses"""
    try:
        data = request.get_json()
        assessment_config = data.get('assessment_config')
        user_responses = data.get('responses')
        
        # Evaluate SJT responses
        evaluation = sjt_engine.evaluate_sjt_responses(assessment_config, user_responses)
        
        # Save to database
        assessment_data = {
            'assessment_type': 'situational_judgment',
            'assessment_config': assessment_config,
            'user_responses': user_responses,
            'evaluation_results': evaluation
        }
        db_manager.save_assessment_result(int(current_user.id), assessment_data)
        
        return jsonify({
            'success': True,
            'evaluation': evaluation
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error evaluating SJT: {str(e)}'})

@app.route('/resume-scorer')
@login_required
@student_required
def resume_scorer_page():
    """Resume analysis and scoring page"""
    return render_template('student/resume_scorer.html')

@app.route('/upload-resume', methods=['POST'])
@login_required
@student_required
def upload_resume():
    """Upload and analyze resume"""
    try:
        from werkzeug.utils import secure_filename
        import os
        
        if 'resume_file' not in request.files:
            return jsonify({'success': False, 'message': 'No file uploaded'})
        
        file = request.files['resume_file']
        job_description = request.form.get('job_description', '')
        
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'})
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', f"{current_user.id}_{filename}")
        os.makedirs('uploads', exist_ok=True)
        file.save(file_path)
        
        # Extract text from resume
        resume_text = resume_scorer.extract_text_from_file(file_path)
        
        # Analyze resume
        analysis = resume_scorer.analyze_resume(resume_text, job_description)
        
        # Save to database
        assessment_data = {
            'assessment_type': 'resume_analysis',
            'file_path': file_path,
            'analysis_results': analysis,
            'job_description': job_description
        }
        db_manager.save_assessment_result(int(current_user.id), assessment_data)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error analyzing resume: {str(e)}'})

@app.route('/mock-interview')
@login_required
@student_required
def mock_interview():
    """Mock interview simulator"""
    return render_template('student/mock_interview.html')

@app.route('/start-mock-interview', methods=['POST'])
@login_required
@student_required
def start_mock_interview():
    """Start mock interview session"""
    try:
        data = request.get_json()
        interview_type = data.get('interview_type', 'behavioral')  # behavioral, technical, mixed
        company_focus = data.get('company_focus', 'general')
        
        # Generate interview session
        session_config = interview_simulator.generate_interview_session(
            interview_type=interview_type,
            company_focus=company_focus,
            num_questions=8
        )
        
        return jsonify({
            'success': True,
            'session_config': session_config,
            'session_id': f"interview_{current_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error starting interview: {str(e)}'})

@app.route('/submit-interview-response', methods=['POST'])
@login_required
@student_required
def submit_interview_response():
    """Submit response to interview question"""
    try:
        data = request.get_json()
        session_config = data.get('session_config')
        question = data.get('question')
        response = data.get('response')
        response_time = data.get('response_time', 0)
        
        # Evaluate response
        evaluation = interview_simulator.evaluate_response(
            session_config, question, response, response_time
        )
        
        return jsonify({
            'success': True,
            'evaluation': evaluation
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error evaluating response: {str(e)}'})

@app.route('/complete-mock-interview', methods=['POST'])
@login_required
@student_required
def complete_mock_interview():
    """Complete mock interview session"""
    try:
        data = request.get_json()
        session_config = data.get('session_config')
        all_responses = data.get('responses')
        
        # Generate overall performance analysis
        performance_analysis = interview_simulator.analyze_overall_performance(
            session_config, all_responses
        )
        
        # Save to database
        assessment_data = {
            'assessment_type': 'mock_interview',
            'session_config': session_config,
            'responses': all_responses,
            'performance_analysis': performance_analysis
        }
        db_manager.save_assessment_result(int(current_user.id), assessment_data)
        
        return jsonify({
            'success': True,
            'performance_analysis': performance_analysis
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error completing interview: {str(e)}'})

# ===== TRUST BUT VERIFY - SKILL VERIFICATION ROUTES =====

@app.route('/skill-verification')
@login_required
@student_required
def skill_verification_hub():
    """Main skill verification hub"""
    return render_template('student/skill_verification.html')

@app.route('/extract-skills-from-resume', methods=['POST'])
@login_required
@student_required
def extract_skills_from_resume():
    """Extract skills from uploaded resume for verification"""
    try:
        from werkzeug.utils import secure_filename
        import os
        
        if 'resume_file' not in request.files:
            return jsonify({'success': False, 'message': 'No resume file uploaded'})
        
        file = request.files['resume_file']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'})
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_path = os.path.join('uploads', f"temp_{current_user.id}_{filename}")
        os.makedirs('uploads', exist_ok=True)
        file.save(temp_path)
        
        # Extract text from resume
        resume_text = resume_scorer.extract_text_from_file(temp_path)
        
        # Extract skills using verification engine
        extracted_skills = verification_engine.extract_skills_from_resume(resume_text)
        
        # Generate verification queue
        verification_queue = verification_engine.generate_verification_queue(
            int(current_user.id), extracted_skills
        )
        
        # Get priority recommendations from badge system
        priority_queue = badge_system.get_verification_queue_priority(
            int(current_user.id), extracted_skills
        )
        
        # Clean up temp file
        try:
            os.unlink(temp_path)
        except:
            pass
        
        return jsonify({
            'success': True,
            'extracted_skills': extracted_skills,
            'verification_queue': verification_queue,
            'priority_recommendations': priority_queue[:10]  # Top 10 priorities
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error extracting skills: {str(e)}'})

@app.route('/start-skill-verification', methods=['POST'])
@login_required
@student_required
def start_skill_verification():
    """Start skill verification challenge"""
    try:
        data = request.get_json()
        skill_name = data.get('skill_name')
        category = data.get('category')
        difficulty = data.get('difficulty', 'medium')
        
        # Start proctored session
        session_id = f"verify_{current_user.id}_{skill_name}_{int(time.time())}"
        proctoring_result = proctoring_system.start_proctored_session(
            user_id=int(current_user.id),
            assessment_type=f'skill_verification_{category}',
            time_limit=900,  # 15 minutes
            session_id=session_id
        )
        
        # Generate appropriate challenge based on category
        if category == 'programming_languages':
            challenge_result = live_coding_manager.start_coding_session(
                user_id=int(current_user.id),
                skill=skill_name,
                difficulty=difficulty
            )
        elif category == 'databases':
            challenge = sql_sandbox.get_sql_challenge(difficulty=difficulty)
            challenge_result = {
                'success': True,
                'challenge': challenge,
                'session_id': session_id
            }
        elif category == 'frameworks_libraries':
            challenge = framework_engine.get_framework_challenge(
                framework=skill_name,
                difficulty=difficulty,
                challenge_type='bug_identification'
            )
            challenge_result = {
                'success': True,
                'challenge': challenge,
                'session_id': session_id
            }
        else:
            # Generic challenge
            challenge = verification_engine.get_verification_challenge(
                skill_name, category, difficulty
            )
            challenge_result = {
                'success': True,
                'challenge': challenge,
                'session_id': session_id
            }
        
        if challenge_result['success']:
            return jsonify({
                'success': True,
                'session_id': session_id,
                'challenge': challenge_result.get('challenge'),
                'proctoring_config': proctoring_result.get('proctoring_config'),
                'monitoring_script': proctoring_result.get('monitoring_script')
            })
        else:
            return jsonify({
                'success': False,
                'message': challenge_result.get('error', 'Failed to generate challenge')
            })
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error starting verification: {str(e)}'})

@app.route('/submit-skill-verification', methods=['POST'])
@login_required
@student_required
def submit_skill_verification():
    """Submit skill verification challenge response"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        skill_name = data.get('skill_name')
        category = data.get('category')
        verification_method = data.get('verification_method', 'live_coding')
        challenge_response = data.get('response')
        
        # End proctored session and get integrity report
        proctoring_result = proctoring_system.end_proctored_session(session_id)
        integrity_report = proctoring_result.get('integrity_report', {})
        
        # Process verification based on method
        if verification_method == 'live_coding':
            # Submit to live coding manager
            evaluation_result = live_coding_manager.submit_code(
                session_id, challenge_response.get('code', '')
            )
        elif verification_method == 'sql_sandbox':
            # Verify SQL challenge
            evaluation_result = sql_sandbox.verify_sql_challenge(
                challenge_response.get('query', ''),
                challenge_response.get('expected_result', []),
                challenge_response.get('schema_name', 'student_courses')
            )
        elif verification_method == 'code_review':
            # Evaluate framework challenge
            evaluation_result = framework_engine.evaluate_code_review_response(
                challenge_response.get('challenge', {}),
                challenge_response
            )
        else:
            # Generic verification
            evaluation_result = verification_engine.verify_skill(
                int(current_user.id), 
                skill_name,
                challenge_response
            )
        
        # Calculate final verification score considering integrity
        base_score = evaluation_result.get('score', 0)
        integrity_score = integrity_report.get('integrity_score', 100)
        integrity_multiplier = integrity_score / 100
        
        final_score = base_score * integrity_multiplier
        verification_passed = (evaluation_result.get('verification_passed', False) and 
                             integrity_report.get('is_valid', True) and 
                             final_score >= 70)
        
        # Award badge if verification passed
        badge_result = None
        if verification_passed:
            badge_result = badge_system.award_verified_badge(
                user_id=int(current_user.id),
                skill_name=skill_name,
                category=category,
                verification_score=final_score,
                verification_method=verification_method,
                challenge_details={
                    'challenge_response': challenge_response,
                    'evaluation_result': evaluation_result,
                    'integrity_report': integrity_report
                }
            )
        
        return jsonify({
            'success': True,
            'verification_passed': verification_passed,
            'final_score': final_score,
            'base_score': base_score,
            'integrity_score': integrity_score,
            'evaluation_details': evaluation_result,
            'integrity_report': integrity_report,
            'badge_awarded': badge_result.get('badge') if badge_result and badge_result['success'] else None,
            'feedback': evaluation_result.get('feedback', [])
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error processing verification: {str(e)}'})

@app.route('/get-verified-badges')
@login_required
@student_required
def get_verified_badges():
    """Get user's verified skill badges"""
    try:
        badges = badge_system.get_user_badges(int(current_user.id))
        portfolio = badge_system.generate_badge_portfolio(int(current_user.id))
        
        # Convert badges to JSON serializable format
        badges_data = []
        for badge in badges:
            badges_data.append({
                'skill_name': badge.skill_name,
                'category': badge.category,
                'badge_level': badge.badge_level.value,
                'verification_score': badge.verification_score,
                'verification_date': badge.verification_date.isoformat(),
                'verification_method': badge.verification_method,
                'badge_id': badge.badge_id,
                'badge_display': badge_system._generate_badge_display(badge)
            })
        
        return jsonify({
            'success': True,
            'badges': badges_data,
            'portfolio': portfolio
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error getting badges: {str(e)}'})

@app.route('/log-proctor-event/<session_id>', methods=['POST'])
@login_required
@student_required
def log_proctor_event(session_id):
    """Log proctoring event during verification"""
    try:
        event_data = request.get_json()
        event_data['ip_address'] = request.remote_addr
        
        result = proctoring_system.log_proctor_event(session_id, event_data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error logging event: {str(e)}'})

@app.route('/get-weighted-prediction', methods=['POST'])
@login_required
@student_required
def get_weighted_prediction():
    """Get placement prediction with verified skill weights"""
    try:
        # Get base student profile
        profile = db_manager.get_student_profile(int(current_user.id))
        
        if not profile:
            return jsonify({'success': False, 'message': 'Profile not found'})
        
        # Base ML features (exclude output variables)
        base_features = {
            'student_id': profile.get('student_id', f'user_{current_user.id}'),
            'branch': profile.get('branch', 'Computer Science'),
            'cgpa': profile.get('cgpa', 0.0),
            'tenth_percentage': profile.get('tenth_percentage', 0.0),
            'twelfth_percentage': profile.get('twelfth_percentage', 0.0),
            'num_projects': profile.get('num_projects', 0),
            'num_internships': profile.get('num_internships', 0),
            'num_certifications': profile.get('num_certifications', 0),
            'programming_languages': profile.get('programming_languages', ''),
            'leetcode_score': profile.get('leetcode_score', 0),
            'codechef_rating': profile.get('codechef_rating', 0),
            'communication_score': profile.get('communication_score', 0.0),
            'leadership_score': profile.get('leadership_score', 0.0),
            'num_hackathons': profile.get('num_hackathons', 0),
            'club_participation': profile.get('club_participation', 0),
            'online_courses': profile.get('online_courses', 0)
        }
        
        # Apply verified skill weights
        weighted_features = badge_system.calculate_weighted_ml_features(
            int(current_user.id), base_features
        )
        
        # Make prediction with weighted features
        if USE_DEEP_MODEL:
            result = deep_predictor.predict(weighted_features)
            model_used = 'deep_learning_verified'
        else:
            result = predictor.predict_placement(weighted_features)
            model_used = 'random_forest_verified'
        
        # Calculate trust score
        badges = badge_system.get_user_badges(int(current_user.id))
        trust_score = badge_system._calculate_trust_score(badges)
        
        # Use safe_jsonify to handle any NaN values in the response
        response_data = {
            'success': True,
            'probability': result['probability'],
            'prediction': result.get('prediction', int(result['probability'] > 0.5)),
            'placement_chance': f"{result['probability']*100:.1f}%",
            'confidence': result.get('confidence', result['probability']),
            'model_used': model_used,
            'trust_score': trust_score,
            'verified_skills_count': len(badges),
            'skill_boost': weighted_features.get('trust_score', 0),
            'verification_confidence': weighted_features.get('verification_coverage', 0) * 100
        }
        
        return jsonify(safe_jsonify(response_data))
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error in weighted prediction: {str(e)}'})

# === CAREER GUIDANCE FEATURES ===

@app.route('/api/ats-analyze', methods=['POST'])
@login_required
@student_required
def ats_analyze_resume():
    """ATS Resume Analysis and Profile Autofill"""
    try:
        if 'resume_file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'})
        
        file = request.files['resume_file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        # Save uploaded file temporarily
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            file.save(tmp_file.name)
            
            # Analyze resume
            result = ats_analyzer.analyze_resume_complete(tmp_file.name)
            
            # Clean up temp file
            os.unlink(tmp_file.name)
            
            return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/chatbot', methods=['POST'])
@login_required
@student_required
def chatbot_message():
    """Process chatbot conversation"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        context = data.get('context', {})
        
        if not message:
            return jsonify({'success': False, 'error': 'Empty message'})
        
        # Process message
        response = ai_chatbot.process_message(
            user_id=int(current_user.id),
            message=message,
            context=context
        )
        
        return jsonify({
            'success': True,
            'response': response
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/search', methods=['GET'])
@login_required
@student_required
def smart_search():
    """Smart Search across learning resources, skills, and jobs"""
    try:
        query = request.args.get('q', '')
        search_type = request.args.get('type', 'all')
        
        # Parse filters
        filters = {}
        if request.args.get('difficulty'):
            filters['difficulty'] = request.args.get('difficulty')
        if request.args.get('content_type'):
            filters['content_type'] = request.args.get('content_type')
        if request.args.get('max_duration'):
            filters['max_duration'] = int(request.args.get('max_duration'))
        
        # Perform search
        result = smart_search.search_all(
            query=query,
            user_id=int(current_user.id),
            filters=filters
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/predict-companies', methods=['POST'])
@login_required
@student_required
def predict_company_tiers():
    """Predict company tiers and role recommendations"""
    try:
        # Get company tier predictions
        result = company_predictor.predict_company_tiers(
            user_id=int(current_user.id)
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/job-fit-analysis', methods=['POST'])
@login_required
@student_required
def analyze_job_fit():
    """Analyze fit for a specific job posting"""
    try:
        data = request.get_json()
        job_details = data.get('job_details', {})
        
        # Get user profile for analysis
        user_profile = company_predictor._get_user_profile(int(current_user.id))
        
        if not user_profile:
            return jsonify({'success': False, 'error': 'User profile not found'})
        
        # Simulate job fit analysis
        fit_analysis = company_predictor._analyze_job_fit(job_details, user_profile)
        
        return jsonify({
            'success': True,
            'fit_analysis': fit_analysis
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
        return jsonify({'success': False, 'message': f'Prediction error: {str(e)}'})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

# Template functions
@app.template_filter('datetime')
def datetime_filter(timestamp):
    """Format datetime for templates"""
    if timestamp:
        return datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').strftime('%B %d, %Y at %I:%M %p')
    return 'Never'

@app.template_filter('percentage')
def percentage_filter(value):
    """Format percentage for templates"""
    return f"{value*100:.1f}%" if value else "0%"

@app.context_processor
def inject_current_time():
    """Make current time available to all templates"""
    return {'current_time': datetime.now()}

def create_industry_templates():
    """Create comprehensive HTML templates"""
    import os
    
    # Create template directories
    template_dirs = [
        'templates',
        'templates/auth',
        'templates/student', 
        'templates/admin',
        'templates/errors'
    ]
    
    for dir_path in template_dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    # Only create missing templates - don't overwrite existing ones
    templates_to_check = {
        'templates/auth/login.html': True,  # Always create login
        'templates/student/profile.html': False,  # Check if exists
        'templates/student/prediction.html': False,
        'templates/student/skill_assessment.html': False,
        'templates/student/courses.html': False,
        'templates/admin/analytics.html': False
    }
    
    # Check which templates are missing
    missing_templates = []
    for template_path, force_create in templates_to_check.items():
        if force_create or not os.path.exists(template_path):
            missing_templates.append(template_path)
    
    if missing_templates:
        print(f"🔧 Creating {len(missing_templates)} missing templates...")
        for template in missing_templates:
            print(f"   Creating {template}")
    
    # Create login template
    login_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔐 Login - Placement Prediction System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
            max-width: 400px;
            width: 100%;
        }
        .login-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .login-form {
            padding: 30px;
        }
        .form-control {
            border-radius: 10px;
            border: 2px solid #e9ecef;
            padding: 12px 15px;
        }
        .form-control:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
        }
        .btn-login {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 10px;
            padding: 12px;
            font-weight: 600;
            width: 100%;
        }
        .btn-login:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <h2><i class="fas fa-graduation-cap"></i> Placement Predictor</h2>
            <p>Sign in to your account</p>
        </div>
        <div class="login-form">
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ 'danger' if category == 'error' else 'success' }} alert-dismissible fade show">
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            
            <form method="POST">
                <div class="mb-3">
                    <label for="email" class="form-label">Email Address</label>
                    <div class="input-group">
                        <span class="input-group-text"><i class="fas fa-envelope"></i></span>
                        <input type="email" class="form-control" id="email" name="email" required>
                    </div>
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <div class="input-group">
                        <span class="input-group-text"><i class="fas fa-lock"></i></span>
                        <input type="password" class="form-control" id="password" name="password" required>
                    </div>
                </div>
                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="remember_me" name="remember_me">
                    <label class="form-check-label" for="remember_me">Remember me</label>
                </div>
                <button type="submit" class="btn btn-primary btn-login">
                    <i class="fas fa-sign-in-alt"></i> Sign In
                </button>
            </form>
            <div class="text-center mt-3">
                <p>Don't have an account? <a href="{{ url_for('auth.register') }}" class="text-decoration-none">Register here</a></p>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
    """
    
    with open('templates/auth/login.html', 'w', encoding='utf-8') as f:
        f.write(login_html)
    
    print("✅ Industry templates created successfully!")

if __name__ == '__main__':
    # Initialize database
    print("🗄️ Initializing database...")
    
    # Create templates
    create_industry_templates()
    
    # Create admin user if doesn't exist
    admin_result = db_manager.create_user(
        email='admin@placement.system',
        password='admin123',
        first_name='System',
        last_name='Administrator',
        user_type='admin'
    )
    
    if admin_result['success']:
        print("👤 Admin user created: admin@placement.system / admin123")
    
    # Run Flask app
    print("🚀 Starting Industry-Ready Flask Application...")
    print("🌐 Open http://localhost:5000 in your browser")
    print("👤 Admin Login: admin@placement.system / admin123")
    
    app.run(debug=True, host='0.0.0.0', port=5000)