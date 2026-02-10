"""
Stellar Compass - Windows Desktop Application
Works with your existing backend/app.py
"""

import webbrowser
import subprocess
import sys
import os
import time
import threading
from pathlib import Path

def start_flask():
    """Start Flask server"""
    try:
        # Get the directory where this script is located
        script_dir = Path(__file__).parent.absolute()
        backend_dir = script_dir / 'backend'
        
        # Add backend directory to Python path
        if str(backend_dir) not in sys.path:
            sys.path.insert(0, str(backend_dir))
        
        # Change to backend directory
        os.chdir(str(backend_dir))
        
        # Import and run the Flask app
        import app
        app.app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False, threaded=True)
        
    except Exception as e:
        print(f"\n❌ Error starting backend: {e}")
        print("\n🔍 Troubleshooting:")
        print(f"   Script directory: {Path(__file__).parent}")
        print(f"   Backend directory: {Path(__file__).parent / 'backend'}")
        print(f"   Looking for: backend/app.py")
        print("\n💡 Make sure:")
        print("   1. backend/app.py exists")
        print("   2. All dependencies are installed")
        print("   3. .env file is in backend/ folder")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)

def main():
    """Main entry point"""
    print("""
    ╔════════════════════════════════════════════════╗
    ║   🌟 Stellar Compass Desktop App 🌟          ║
    ╚════════════════════════════════════════════════╝
    """)
    
    # Get script directory
    script_dir = Path(__file__).parent.absolute()
    
    # Check if backend folder exists
    backend_folder = script_dir / 'backend'
    if not backend_folder.exists():
        print(f"❌ Error: backend folder not found!")
        print(f"   Expected: {backend_folder}")
        print(f"\n💡 Make sure you're running this from the project root folder")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Check if app.py exists
    app_file = backend_folder / 'app.py'
    if not app_file.exists():
        print(f"❌ Error: backend/app.py not found!")
        print(f"   Expected: {app_file}")
        print(f"\n💡 Download the app.py file and place it in backend/ folder")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print("🚀 Starting application...")
    print(f"📁 Project directory: {script_dir}")
    print(f"📁 Backend directory: {backend_folder}")
    
    # Start Flask in background
    print("\n⏳ Starting backend server...")
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    
    # Wait for server to start
    print("⏳ Initializing (this takes a few seconds)...")
    for i in range(5, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    # Test if server is running
    try:
        import urllib.request
        urllib.request.urlopen('http://127.0.0.1:5000/health', timeout=2)
        print("✅ Backend is running!")
    except:
        print("⚠️  Backend might still be starting...")
    
    # Open in browser (app mode)
    print("\n🌐 Opening application window...")
    
    url = 'http://127.0.0.1:5000'
    
    # Try to open in browser 'app' mode (Chrome or Edge) for a desktop-like window.
    browser_path = None
    possible_browser_paths = [
        # Chrome
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        os.path.expanduser(r'~\AppData\Local\Google\Chrome\Application\chrome.exe'),
        # Edge
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
        os.path.expanduser(r'~\AppData\Local\Microsoft\Edge\Application\msedge.exe'),
    ]

    for path in possible_browser_paths:
        if os.path.exists(path):
            browser_path = path
            break

    if browser_path:
        try:
            # Launch directly using subprocess (more reliable than `start` for --app)
            subprocess.Popen([
                browser_path,
                f'--app={url}',
                '--new-window',
                '--window-size=1200,800'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)

            print("✅ Application opened in app mode")

        except Exception:
            # Fallback to start (older Windows behavior)
            try:
                os.system(f'start "" "{browser_path}" --app={url} --window-size=1200,800 --new-window')
                print("✅ Application opened (fallback start)")
            except Exception:
                webbrowser.open(url)
                print("✅ Application opened in default browser")
                print("💡 Tip: Install Chrome or Edge for the best desktop app experience")
    else:
        # No supported browser found, open default
        webbrowser.open(url)
        print("✅ Application opened in default browser")
        print("💡 Tip: Install Chrome or Edge for the best desktop app experience")
    
    print("\n" + "=" * 50)
    print("✅ Stellar Compass is running!")
    print("=" * 50)
    print("\n📝 Instructions:")
    print("   • Your app is now open in a window")
    print("   • Keep this console window open")
    print("   • Close this window to stop the app")
    print(f"\n🌐 URL: {url}")
    print("\n💡 Tips:")
    print("   • Test notifications: {url}/test-notification")
    print("   • Health check: {url}/health")
    print("\nPress Ctrl+C to quit\n")
    
    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 Closing Stellar Compass... Goodbye!")
        sys.exit(0)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)
