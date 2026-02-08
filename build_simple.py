"""
Build Stellar Compass Windows Desktop App
Simple launcher version (no compilation issues!)
"""

import PyInstaller.__main__
import os
from pathlib import Path

def build_exe():
    """Build Windows executable"""
    
    print("""
    ╔════════════════════════════════════════════════╗
    ║   🔨 Building Stellar Compass Desktop App    ║
    ╚════════════════════════════════════════════════╝
    """)
    
    project_dir = Path(__file__).parent
    
    # Simple PyInstaller build
    args = [
        'stellar_compass.py',
        '--name=StellarCompass',
        '--onefile',
        '--console',  # Show console with startup info
        
        # Include data folders
        '--add-data=frontend;frontend',
        '--add-data=backend;backend',
        
        # Hidden imports
        '--hidden-import=flask',
        '--hidden-import=flask_cors',
        '--hidden-import=stellar_sdk',
        '--hidden-import=dotenv',
        '--hidden-import=email.mime.text',
        '--hidden-import=email.mime.multipart',
        
        # Clean build
        '--clean',
        '--noconfirm'
    ]
    
    # Add icon if exists
    if os.path.exists('icon.ico'):
        args.append('--icon=icon.ico')
        print("📦 Building with custom icon...")
    else:
        print("📦 Building without icon (create icon.ico for custom icon)")
    
    print("\n🔨 Running PyInstaller...")
    print("⏳ This may take 2-3 minutes...\n")
    
    PyInstaller.__main__.run(args)
    
    print("\n" + "=" * 50)
    print("✅ BUILD COMPLETE!")
    print("=" * 50)
    print(f"\n📁 Executable: {project_dir / 'dist' / 'StellarCompass.exe'}")
    print(f"📏 Size: ~40-50MB")
    print("\n📝 To distribute:")
    print("   1. Copy dist/StellarCompass.exe")
    print("   2. Create .env file in same folder as .exe")
    print("   3. Share both files")
    print("\n🚀 Double-click StellarCompass.exe to run!")
    print("\n" + "=" * 50)

if __name__ == '__main__':
    build_exe()
