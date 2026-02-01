"""
Build script for creating standalone EXE using PyInstaller.
Run this script to build the application.
"""
import subprocess
import sys
import os

def build():
    # Ensure PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build command
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--name=UrduTranslator",
        "--onefile",
        "--windowed",
        "--clean",
        "--noconfirm",
        # Add icon if exists
        # "--icon=icon.ico",
        "main.py"
    ]
    
    print("Building EXE...")
    print("Command:", " ".join(cmd))
    
    # Run PyInstaller
    result = subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(__file__)))
    
    if result.returncode == 0:
        print("\n✓ Build successful!")
        print("EXE location: dist/UrduTranslator.exe")
    else:
        print("\n✗ Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    build()
