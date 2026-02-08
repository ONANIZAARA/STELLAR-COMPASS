# Build Script for Stellar Compass Windows App
# This creates a standalone .exe file

import PyInstaller.__main__
import os
import shutil
from pathlib import Path

def build_exe():
    """Build Windows executable"""
    
    print("🔨 Building Stellar Compass Windows Application...")
    print("-" * 50)
    
    # Get project directory
    project_dir = Path(__file__).parent
    
    # PyInstaller arguments
    args = [
        'desktop_app.py',  # Main file
        '--name=StellarCompass',  # App name
        '--onefile',  # Single executable
        '--windowed',  # No console window
        '--icon=icon.ico',  # App icon (create this)
        
        # Include data files
        '--add-data=frontend;frontend',
        '--add-data=backend;backend',
        '--add-data=.env;.',
        
        # Hidden imports
        '--hidden-import=flask',
        '--hidden-import=stellar_sdk',
        '--hidden-import=webview',
        '--hidden-import=dotenv',
        
        # Exclude unnecessary modules
        '--exclude-module=matplotlib',
        '--exclude-module=numpy',
        '--exclude-module=pandas',
        
        # Output directory
        '--distpath=dist',
        '--workpath=build',
        '--specpath=.',
        
        # Clean build
        '--clean',
        
        # No confirmation
        '--noconfirm'
    ]
    
    print("📦 Running PyInstaller...")
    PyInstaller.__main__.run(args)
    
    print("\n✅ Build complete!")
    print(f"📁 Executable location: {project_dir / 'dist' / 'StellarCompass.exe'}")
    print("\n📝 Next steps:")
    print("1. Copy the .env file to the same folder as the .exe")
    print("2. Run StellarCompass.exe")
    print("3. Enjoy! 🎉")

if __name__ == '__main__':
    build_exe()
