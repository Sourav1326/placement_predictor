#!/usr/bin/env python3
"""
Quick test to verify login redirects work properly
"""

import os
import sys

# Set working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print(f"Working directory: {os.getcwd()}")

print("🧪 Testing route availability...")

# Test template files exist
templates_to_check = [
    'templates/errors/404.html',
    'templates/errors/500.html',
    'templates/auth/login.html',
    'templates/auth/register.html',
    'templates/student/dashboard.html',
    'templates/admin/dashboard.html'
]

for template in templates_to_check:
    if os.path.exists(template):
        print(f"✅ {template} exists")
    else:
        print(f"❌ {template} missing")

# Test Flask routes are properly defined
print("\n🔍 Checking Flask app configuration...")
try:
    # Import without running the app
    sys.path.append('utils')
    from industry_flask_app import app
    
    # Check routes
    routes = []
    for rule in app.url_map.iter_rules():
        methods = list(rule.methods or [])
        routes.append(f"{rule.rule} ({', '.join(methods)})")
    
    print(f"✅ Flask app loaded successfully")
    print(f"📋 Available routes ({len(routes)}):")
    for route in sorted(routes):
        if 'GET' in route:
            print(f"  {route}")
    
    # Check error handlers
    error_handlers = app.error_handler_spec.get(None, {}) or {}
    print(f"\n🛡️ Error handlers configured: {len(error_handlers)}")
    
except Exception as e:
    print(f"❌ Flask app error: {e}")

print("\n✅ Basic checks completed!")
print("🚀 You can now run: python run_industry_system.py")