#!/usr/bin/env python3
"""
Auto-installer for Placement Predictor System
Checks system requirements and installs Python if needed
"""

import os
import sys
import platform
import subprocess
import urllib.request
import shutil
from pathlib import Path

def check_python_installation():
    """Check if Python is properly installed"""
    try:
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            print(f"✅ Python {version.major}.{version.minor}.{version.micro} is installed")
            return True
        else:
            print(f"❌ Python {version.major}.{version.minor}.{version.micro} is too old (need 3.8+)")
            return False
    except:
        print("❌ Python not found")
        return False

def get_python_download_url():
    """Get appropriate Python download URL based on system"""
    system = platform.system().lower()
    architecture = platform.machine().lower()
    
    if system == "windows":
        if "64" in architecture or "amd64" in architecture:
            return "https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"
        else:
            return "https://www.python.org/ftp/python/3.11.7/python-3.11.7.exe"
    elif system == "darwin":  # macOS
        return "https://www.python.org/ftp/python/3.11.7/python-3.11.7-macos11.pkg"
    else:  # Linux
        return None  # Use package manager

def provide_installation_instructions():
    """Provide Python installation instructions for all platforms"""
    system = platform.system().lower()
    
    print("\n📝 Python Installation Instructions:")
    print("="*50)
    
    if system == "windows":
        print("💻 Windows:")
        print("1. Go to https://www.python.org/downloads/")
        print("2. Click 'Download Python 3.11.x'")
        print("3. Run the installer")
        print("4. ✅ IMPORTANT: Check 'Add Python to PATH'")
        print("5. Click 'Install Now'")
        print("6. Restart command prompt/PowerShell")
    
    elif system == "darwin":
        print("🍎 macOS:")
        print("Option 1 - Official installer:")
        print("1. Go to https://www.python.org/downloads/")
        print("2. Download macOS installer")
        print("3. Run the .pkg file")
        print("")
        print("Option 2 - Homebrew (if installed):")
        print("  brew install python@3.11")
    
    else:
        print("🐧 Linux:")
        print("Ubuntu/Debian:")
        print("  sudo apt update && sudo apt install python3 python3-pip python3-venv")
        print("")
        print("CentOS/RHEL/Fedora:")
        print("  sudo dnf install python3 python3-pip")
        print("")
        print("Arch Linux:")
        print("  sudo pacman -S python python-pip")
    
    print("\n✨ After installation, run this script again!")

def main():
    """Main function"""
    print("🐍 Python Auto-Installer for Placement Predictor System")
    print("="*60)
    
    # Check if Python is already installed
    if check_python_installation():
        print("\n🎉 Python is ready! Starting main setup...")
        
        # Run the main setup script
        try:
            if os.path.exists('one_click_setup.py'):
                subprocess.run([sys.executable, 'one_click_setup.py'])
            elif os.path.exists('QUICK_START.py'):
                subprocess.run([sys.executable, 'QUICK_START.py'])
            else:
                print("❌ Setup scripts not found")
        except Exception as e:
            print(f"❌ Setup failed: {e}")
        
        return
    
    # Python not installed, offer to install
    print("\n❌ Python 3.8+ is required but not found")
    print("\nOptions:")
    print("1. Auto-install Python (Windows/macOS)")
    print("2. Get manual installation instructions")
    print("3. Exit and install manually")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        provide_installation_instructions()
    
    elif choice == "2":
        provide_installation_instructions()
        print("\n📋 Manual Installation Instructions:")
        print("1. Go to https://www.python.org/downloads/")
        print("2. Download Python 3.8 or newer")
        print("3. During installation, check 'Add Python to PATH'")
        print("4. Restart your command prompt/terminal")
        print("5. Run this script again")
    
    else:
        print("👋 Please install Python manually and run this script again")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Installation cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("Press Enter to exit...")