"""
Simple Flask-based web interface for Placement Prediction System
Alternative to Streamlit for quick testing and demonstration
"""

from flask import Flask, render_template, request, jsonify, session
import sys
import os
import json

# Add utils to path
sys.path.append('utils')

try:
    from src.model_training import PlacementPredictor
    from skill_assessment import SkillAssessmentEngine
    from course_recommendation_engine import CourseRecommendationEngine
    from recommendations import PlacementRecommendationEngine
    import pandas as pd
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all required modules are available")

app = Flask(__name__)
app.secret_key = 'placement_predictor_secret_key'

# Initialize all engines
predictor = PlacementPredictor()
predictor.load_models()

skill_engine = SkillAssessmentEngine()
course_engine = CourseRecommendationEngine()
recommendation_engine = PlacementRecommendationEngine()

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Prediction endpoint"""
    try:
        # Get data from form
        data = request.get_json()
        
        # Prepare student data
        student_data = {
            'student_id': 'WEB001',
            'branch': data.get('branch', 'Computer Science'),
            'cgpa': float(data.get('cgpa', 7.5)),
            'tenth_percentage': float(data.get('tenth_percentage', 85.0)),
            'twelfth_percentage': float(data.get('twelfth_percentage', 85.0)),
            'num_projects': int(data.get('num_projects', 2)),
            'num_internships': int(data.get('num_internships', 1)),
            'num_certifications': int(data.get('num_certifications', 1)),
            'programming_languages': data.get('programming_languages', 'Python, Java'),
            'leetcode_score': int(data.get('leetcode_score', 1200)),
            'codechef_rating': int(data.get('codechef_rating', 1400)),
            'communication_score': float(data.get('communication_score', 7.0)),
            'leadership_score': float(data.get('leadership_score', 6.0)),
            'num_hackathons': int(data.get('num_hackathons', 1)),
            'club_participation': int(data.get('club_participation', 1)),
            'online_courses': int(data.get('online_courses', 2)),
            'placed': 0,
            'salary_package': 0,
            'package_category': 'Unknown'
        }
        
        # Make prediction
        result = predictor.predict_placement(student_data)
        
        if result:
            # Get feature importance if available
            feature_impact = None
            try:
                feature_impact = predictor.get_feature_importance_for_prediction(student_data)
                if feature_impact:
                    # Convert to list of top 5 features
                    top_features = list(feature_impact.items())[:5]
                    feature_impact = [
                        {
                            'feature': feature.replace('_', ' ').title(),
                            'importance': details['importance'],
                            'value': details['value']
                        }
                        for feature, details in top_features
                    ]
            except:
                feature_impact = None
            
            return jsonify({
                'success': True,
                'probability': result['probability'],
                'prediction': result['prediction'],
                'placement_chance': result['placement_chance'],
                'feature_importance': feature_impact
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Prediction failed'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/skill-assessment')
def skill_assessment():
    """Skill assessment page"""
    return render_template('skill_assessment.html')

@app.route('/conduct-assessment', methods=['POST'])
def conduct_assessment():
    """Conduct skill assessment quiz"""
    try:
        data = request.get_json()
        languages = data.get('languages', []).split(',')
        languages = [lang.strip() for lang in languages if lang.strip()]
        
        # Conduct assessment
        assessment_results = skill_engine.conduct_skill_assessment(languages, questions_per_level=3)
        skill_report = skill_engine.generate_skill_report(assessment_results)
        
        # Store in session for later use
        session['skill_assessment'] = {
            'results': assessment_results,
            'report': skill_report
        }
        
        return jsonify({
            'success': True,
            'report': skill_report,
            'detailed_results': assessment_results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Assessment error: {str(e)}'
        })

@app.route('/course-recommendations')
def course_recommendations():
    """Course recommendations page"""
    return render_template('course_recommendations.html')

@app.route('/get-course-recommendations', methods=['POST'])
def get_course_recommendations():
    """Get personalized course recommendations"""
    try:
        data = request.get_json()
        
        # Build student profile
        student_profile = {
            'programming_languages': data.get('programming_languages', ''),
            'num_projects': int(data.get('num_projects', 0)),
            'num_internships': int(data.get('num_internships', 0)),
            'leetcode_score': int(data.get('leetcode_score', 0)),
            'cgpa': float(data.get('cgpa', 7.0))
        }
        
        target_companies = data.get('target_companies', [])
        
        # Get course recommendations
        recommendations = course_engine.recommend_courses_for_student(
            student_profile, target_companies
        )
        
        return jsonify({
            'success': True,
            'recommendations': {
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
                    for company, courses in recommendations['company_specific'].items()
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Recommendation error: {str(e)}'
        })
    """Analytics dashboard"""
    try:
        # Load dataset for analytics
        if os.path.exists('data/placement_data.csv'):
            df = pd.read_csv('data/placement_data.csv')
            
            stats = {
                'total_students': len(df),
                'placed_students': int(df['placed'].sum()),
                'placement_rate': float(df['placed'].mean()),
                'avg_cgpa': float(df['cgpa'].mean()),
                'branches': df['branch'].value_counts().to_dict(),
                'placement_by_branch': df.groupby('branch')['placed'].agg(['count', 'sum']).to_dict()
            }
            
            return render_template('dashboard.html', stats=stats)
        else:
            return render_template('dashboard.html', stats=None, error="Dataset not found")
    except Exception as e:
        return render_template('dashboard.html', stats=None, error=str(e))

# Create templates directory and files
def create_templates():
    """Create HTML templates"""
    import os
    
    templates_dir = 'templates'
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    
    # Index template
    index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 Placement Prediction System</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .header p { font-size: 1.2rem; opacity: 0.9; }
        .content { padding: 40px; }
        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        .form-section {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            border-left: 5px solid #667eea;
        }
        .form-section h3 {
            margin-bottom: 20px;
            color: #333;
            display: flex;
            align-items: center;
        }
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #555;
        }
        .form-group input, .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #667eea;
        }
        .predict-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: transform 0.3s;
        }
        .predict-btn:hover { transform: translateY(-2px); }
        .result {
            margin-top: 30px;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            display: none;
        }
        .result.success {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
        }
        .result.warning {
            background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
            color: #2d3436;
        }
        .result.danger {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        .probability {
            font-size: 3rem;
            font-weight: bold;
            margin: 10px 0;
        }
        .features {
            margin-top: 20px;
            text-align: left;
        }
        .feature-item {
            background: rgba(255,255,255,0.2);
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
        }
        .nav {
            background: rgba(255,255,255,0.1);
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .nav a {
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 8px;
            transition: background 0.3s;
        }
        .nav a:hover { background: rgba(255,255,255,0.2); }
        @media (max-width: 768px) {
            .form-grid { grid-template-columns: 1fr; }
            .header h1 { font-size: 2rem; }
            .content { padding: 20px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="nav">
                <div>🎯 Placement Predictor</div>
                <div>
                    <a href="/">🏠 Home</a>
                    <a href="/dashboard">📊 Dashboard</a>
                </div>
            </div>
            <h1>Placement Prediction System</h1>
            <p>Predict your placement probability with AI-powered analysis</p>
        </div>
        
        <div class="content">
            <form id="predictionForm">
                <div class="form-grid">
                    <div class="form-section">
                        <h3>🎓 Academic Information</h3>
                        <div class="form-group">
                            <label for="cgpa">CGPA (0-10)</label>
                            <input type="number" id="cgpa" name="cgpa" min="0" max="10" step="0.1" value="7.5" required>
                        </div>
                        <div class="form-group">
                            <label for="tenth_percentage">10th Percentage</label>
                            <input type="number" id="tenth_percentage" name="tenth_percentage" min="0" max="100" step="0.1" value="85" required>
                        </div>
                        <div class="form-group">
                            <label for="twelfth_percentage">12th Percentage</label>
                            <input type="number" id="twelfth_percentage" name="twelfth_percentage" min="0" max="100" step="0.1" value="85" required>
                        </div>
                        <div class="form-group">
                            <label for="branch">Branch</label>
                            <select id="branch" name="branch" required>
                                <option value="Computer Science">Computer Science</option>
                                <option value="Information Technology">Information Technology</option>
                                <option value="Electronics">Electronics</option>
                                <option value="Mechanical">Mechanical</option>
                                <option value="Civil">Civil</option>
                                <option value="Electrical">Electrical</option>
                                <option value="Chemical">Chemical</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="form-section">
                        <h3>💻 Technical Skills</h3>
                        <div class="form-group">
                            <label for="num_projects">Number of Projects</label>
                            <input type="number" id="num_projects" name="num_projects" min="0" max="20" value="2" required>
                        </div>
                        <div class="form-group">
                            <label for="num_internships">Number of Internships</label>
                            <input type="number" id="num_internships" name="num_internships" min="0" max="10" value="1" required>
                        </div>
                        <div class="form-group">
                            <label for="num_certifications">Number of Certifications</label>
                            <input type="number" id="num_certifications" name="num_certifications" min="0" max="20" value="1" required>
                        </div>
                        <div class="form-group">
                            <label for="programming_languages">Programming Languages</label>
                            <input type="text" id="programming_languages" name="programming_languages" value="Python, Java" required>
                        </div>
                    </div>
                    
                    <div class="form-section">
                        <h3>🏆 Coding Skills</h3>
                        <div class="form-group">
                            <label for="leetcode_score">LeetCode Score</label>
                            <input type="number" id="leetcode_score" name="leetcode_score" min="0" max="5000" value="1200" required>
                        </div>
                        <div class="form-group">
                            <label for="codechef_rating">CodeChef Rating</label>
                            <input type="number" id="codechef_rating" name="codechef_rating" min="1000" max="3000" value="1400" required>
                        </div>
                        <div class="form-group">
                            <label for="communication_score">Communication Skills (1-10)</label>
                            <input type="number" id="communication_score" name="communication_score" min="1" max="10" step="0.1" value="7" required>
                        </div>
                        <div class="form-group">
                            <label for="leadership_score">Leadership Skills (1-10)</label>
                            <input type="number" id="leadership_score" name="leadership_score" min="1" max="10" step="0.1" value="6" required>
                        </div>
                    </div>
                    
                    <div class="form-section">
                        <h3>🎯 Extracurricular</h3>
                        <div class="form-group">
                            <label for="num_hackathons">Number of Hackathons</label>
                            <input type="number" id="num_hackathons" name="num_hackathons" min="0" max="20" value="1" required>
                        </div>
                        <div class="form-group">
                            <label for="club_participation">Club Participation</label>
                            <input type="number" id="club_participation" name="club_participation" min="0" max="10" value="1" required>
                        </div>
                        <div class="form-group">
                            <label for="online_courses">Online Courses</label>
                            <input type="number" id="online_courses" name="online_courses" min="0" max="50" value="2" required>
                        </div>
                    </div>
                </div>
                
                <button type="submit" class="predict-btn">🚀 Predict Placement Probability</button>
            </form>
            
            <div id="result" class="result">
                <h2 id="result-title"></h2>
                <div class="probability" id="probability"></div>
                <p id="result-message"></p>
                <div class="features" id="features"></div>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('predictionForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this);
            const data = {};
            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }
            
            // Show loading
            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';
            resultDiv.className = 'result';
            resultDiv.innerHTML = '<h2>🔄 Analyzing your profile...</h2>';
            
            // Make prediction request
            fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    const probability = result.probability;
                    const percentage = (probability * 100).toFixed(1);
                    
                    // Determine result class and message
                    let resultClass, title, message;
                    if (probability >= 0.7) {
                        resultClass = 'success';
                        title = '🎉 Excellent Placement Chances!';
                        message = 'You have high chances of getting placed. Keep up the great work!';
                    } else if (probability >= 0.4) {
                        resultClass = 'warning';
                        title = '⚠️ Moderate Placement Chances';
                        message = 'You have decent chances, but there\\'s room for improvement!';
                    } else {
                        resultClass = 'danger';
                        title = '📈 Improvement Needed';
                        message = 'Focus on enhancing your skills and profile for better chances!';
                    }
                    
                    // Show result
                    resultDiv.className = `result ${resultClass}`;
                    resultDiv.innerHTML = `
                        <h2>${title}</h2>
                        <div class="probability">${percentage}%</div>
                        <p>${message}</p>
                        ${result.feature_importance ? `
                            <div class="features">
                                <h3>🔍 Key Influencing Factors:</h3>
                                ${result.feature_importance.map(f => `
                                    <div class="feature-item">
                                        <strong>${f.feature}</strong>: ${(f.importance * 100).toFixed(1)}% influence
                                    </div>
                                `).join('')}
                            </div>
                        ` : ''}
                    `;
                } else {
                    resultDiv.className = 'result danger';
                    resultDiv.innerHTML = `
                        <h2>❌ Prediction Failed</h2>
                        <p>${result.message}</p>
                    `;
                }
            })
            .catch(error => {
                resultDiv.className = 'result danger';
                resultDiv.innerHTML = `
                    <h2>❌ Error</h2>
                    <p>An error occurred: ${error.message}</p>
                `;
            });
        });
    </script>
</body>
</html>
    """
    
    with open(f'{templates_dir}/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    # Dashboard template (simplified)
    dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 Admin Dashboard - Placement Prediction</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .nav {
            background: rgba(255,255,255,0.1);
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .nav a {
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 8px;
            transition: background 0.3s;
        }
        .nav a:hover { background: rgba(255,255,255,0.2); }
        .content { padding: 40px; }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
        }
        .stat-number {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .stat-label {
            font-size: 1.1rem;
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="nav">
                <div>📊 Admin Dashboard</div>
                <div>
                    <a href="/">🏠 Home</a>
                    <a href="/dashboard">📊 Dashboard</a>
                </div>
            </div>
            <h1>Placement Analytics Dashboard</h1>
            <p>Comprehensive insights into placement trends and statistics</p>
        </div>
        
        <div class="content">
            {% if stats %}
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{{ stats.total_students }}</div>
                    <div class="stat-label">Total Students</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ stats.placed_students }}</div>
                    <div class="stat-label">Students Placed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ "%.1f"|format(stats.placement_rate * 100) }}%</div>
                    <div class="stat-label">Placement Rate</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ "%.2f"|format(stats.avg_cgpa) }}</div>
                    <div class="stat-label">Average CGPA</div>
                </div>
            </div>
            
            <div style="background: #f8f9fa; padding: 25px; border-radius: 15px;">
                <h3>📋 Branch-wise Statistics</h3>
                {% for branch, count in stats.branches.items() %}
                <div style="margin: 10px 0; padding: 10px; background: white; border-radius: 8px;">
                    <strong>{{ branch }}</strong>: {{ count }} students
                </div>
                {% endfor %}
            </div>
            {% else %}
            <div style="text-align: center; padding: 50px;">
                <h2>❌ No Data Available</h2>
                <p>{{ error or "Unable to load dashboard data" }}</p>
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
    """
    
    with open(f'{templates_dir}/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(dashboard_html)

if __name__ == '__main__':
    # Create templates
    create_templates()
    
    # Run Flask app
    print("🚀 Starting Flask Web Interface...")
    print("📱 Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)