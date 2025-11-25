#!/usr/bin/env python3
"""
Simple test to check if Flask can discover templates
"""

from flask import Flask, render_template
import os

def test_template_discovery():
    """Test if Flask can find templates"""
    app = Flask(__name__, template_folder='templates')
    
    print("🧪 Testing template discovery...")
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"📁 Template folder: {app.template_folder}")
    template_folder = app.template_folder or 'templates'
    print(f"📁 Template folder absolute: {os.path.abspath(template_folder)}")
    
    # Test with app context
    with app.app_context():
        try:
            # Check if templates exist
            templates_to_test = [
                'student/profile.html',
                'student/prediction.html',
                'student/skill_assessment.html',
                'student/courses.html',
                'admin/analytics.html',
                'admin/dashboard.html'
            ]
            
            for template in templates_to_test:
                template_path = os.path.join(template_folder, template)
                exists = os.path.exists(template_path)
                print(f"{'✅' if exists else '❌'} {template}: {template_path}")
                
                if exists:
                    try:
                        # Try to get the template
                        app.jinja_env.get_template(template)
                        print(f"  ✅ Flask can load {template}")
                    except Exception as e:
                        print(f"  ❌ Flask cannot load {template}: {e}")
        
        except Exception as e:
            print(f"❌ Template discovery error: {e}")

if __name__ == '__main__':
    test_template_discovery()