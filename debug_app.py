import sys
import os

# Add the project root to the path
project_root = os.path.dirname(__file__)
sys.path.insert(0, project_root)

# Set Flask to debug mode
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_DEBUG'] = '1'

try:
    print("Starting application with debug information...")
    print(f"Python path: {sys.executable}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Project root: {project_root}")
    
    # Import and run the main application
    from src.main import app
    
    print("Application imported successfully!")
    print("Starting Flask app...")
    
    # Run with more verbose output
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
    
except Exception as e:
    print(f"Error starting application: {e}")
    import traceback
    traceback.print_exc()