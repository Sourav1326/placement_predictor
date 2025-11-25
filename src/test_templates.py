#!/usr/bin/env python3
"""
Quick Template Test Script
Tests if Flask can find the templates properly
"""

import os
import sys

# Set working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print(f"Working directory: {os.getcwd()}")

# Test template file existence
template_path = os.path.join('templates', 'auth', 'login.html')
print(f"Checking template path: {template_path}")

if os.path.exists(template_path):
    print("✅ Template file exists!")
    print(f"Template size: {os.path.getsize(template_path)} bytes")
else:
    print("❌ Template file not found!")

# Test Flask template discovery
try:
    from flask import Flask
    
    # Test with explicit template folder
    app = Flask(__name__, template_folder='templates')
    
    print("\n🧪 Testing Flask template discovery...")
    
    with app.app_context():
        # Try to get the template
        template = app.jinja_env.get_template('auth/login.html')
        print("✅ Flask can find the template!")
        print(f"Template name: {template.name}")
        print(f"Template filename: {template.filename}")
        
except Exception as e:
    print(f"❌ Flask template error: {e}")

print("\n🔍 Template directory structure:")
if os.path.exists('templates'):
    for root, dirs, files in os.walk('templates'):
        level = root.replace('templates', '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")
else:
    print("❌ Templates directory not found!")

print("\n✅ Template test completed!")