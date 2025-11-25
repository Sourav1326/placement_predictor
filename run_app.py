import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Run the main application
if __name__ == '__main__':
    try:
        from src.main import app
        print("🚀 Starting Industry-Ready Flask Application...")
        print("🌐 Open http://localhost:5000 in your browser")
        print("👤 Admin Login: admin@placement.system / admin123")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()