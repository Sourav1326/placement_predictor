import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(__file__))

def test_environment():
    """Test if all required packages are available in the portable environment"""
    required_packages = [
        'flask',
        'pandas',
        'numpy',
        'sklearn',
        'tensorflow_intel',
        'matplotlib',
        'seaborn',
        'nltk',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'sklearn':
                import sklearn
                print(f"✓ {package} (version: {sklearn.__version__})")
            elif package == 'flask':
                import flask
                print(f"✓ {package} (version: {flask.__version__})")
            elif package == 'tensorflow_intel':
                import tensorflow as tf
                print(f"✓ {package} (version: {tf.__version__})")
            else:
                __import__(package)
                print(f"✓ {package}")
        except ImportError as e:
            print(f"✗ {package} - {e}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        return False
    else:
        print("\n✅ All required packages are available!")
        return True

if __name__ == "__main__":
    print("Testing portable environment...")
    print("=" * 40)
    success = test_environment()
    if success:
        print("\n🎉 Environment is ready for the application!")
    else:
        print("\n❌ Environment is missing some packages.")