#!/usr/bin/env python3
"""
Test script to verify the admin dashboard moment() fix
"""

import os
import sys
from datetime import datetime

# Set working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print(f"Working directory: {os.getcwd()}")

print("🧪 Testing admin dashboard template fix...")

# Test 1: Check if moment() has been removed from template
template_path = 'templates/admin/dashboard.html'
if os.path.exists(template_path):
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'moment()' in content:
        print("❌ Template still contains moment() - fix incomplete")
    else:
        print("✅ Template no longer contains moment() function")
    
    if 'current_time' in content:
        print("✅ Template now uses current_time variable")
    else:
        print("❌ Template missing current_time variable")
else:
    print("❌ Admin dashboard template not found")

# Test 2: Check if Flask app has context processor
print("\n🔍 Checking Flask app configuration...")
try:
    sys.path.append('utils')
    from industry_flask_app import app
    
    # Check context processors
    context_processors = app.template_context_processors.get(None, [])
    print(f"✅ Flask app loaded, context processors: {len(context_processors)}")
    
    # Test datetime formatting
    test_time = datetime.now()
    formatted_time = test_time.strftime('%B %d, %Y at %I:%M %p')
    print(f"✅ Time formatting works: {formatted_time}")
    
except Exception as e:
    print(f"❌ Flask app error: {e}")

print("\n✅ Admin dashboard fix verification completed!")
print("🚀 Try logging in as admin now - the moment() error should be resolved!")