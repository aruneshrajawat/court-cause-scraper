#!/usr/bin/env python3
"""
Quick start script for Flask app
"""
import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✓ Requirements installed")
    except subprocess.CalledProcessError:
        print("✗ Failed to install requirements")
        return False
    return True

def run_flask():
    """Run Flask application"""
    try:
        os.environ['FLASK_APP'] = 'app.py'
        os.environ['FLASK_ENV'] = 'development'
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n✓ Flask app stopped")

if __name__ == '__main__':
    print("Court Scraper Flask App Setup")
    print("=" * 30)
    
    if install_requirements():
        print("\nStarting Flask app...")
        print("Open http://127.0.0.1:5000 in your browser")
        print("Press Ctrl+C to stop")
        run_flask()