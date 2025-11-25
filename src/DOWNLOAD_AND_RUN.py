#!/usr/bin/env python3
"""
Bootstrap Launcher for Placement Predictor System
This minimal script can run with any Python and will download everything needed
"""

print("🎯 Placement Predictor - Bootstrap Launcher")
print("="*50)
print("Checking system and starting universal installer...")

import sys
import subprocess
import urllib.request
import os

def check_internet():
    """Check internet connectivity"""
    try:
        urllib.request.urlopen('https://www.google.com', timeout=5)
        return True
    except:
        return False

def run_universal_installer():
    """Run the universal installer"""
    if os.path.exists('UNIVERSAL_SETUP.py'):
        print("✅ Universal installer found")
        print("🚀 Starting comprehensive setup...")
        subprocess.run([sys.executable, 'UNIVERSAL_SETUP.py'])
    else:
        print("❌ Universal installer not found")
        print("Please ensure UNIVERSAL_SETUP.py is in the same directory")

def main():
    print(f"Python version: {sys.version}")
    
    if not check_internet():
        print("⚠️ No internet connection detected")
        print("Internet is required for downloading dependencies")
        input("Please check your connection and press Enter to continue...")
    
    print("✅ System ready for setup")
    run_universal_installer()

if __name__ == "__main__":
    main()