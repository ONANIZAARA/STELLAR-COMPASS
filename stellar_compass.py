"""
Stellar Compass - Windows Desktop Application
Simple launcher that works with your existing backend/app.py
"""

import webbrowser
import sys
import os
import time
import threading
from pathlib import Path

def start_flask():
    """Start Flask server"""
    try:
        # Add backend to path
        backend_path = Path(__file__).parent / 'backend'
        sys.path.insert(0, str(backend_path))
        
        # Import your existing app.py
        import app
        
        # Run the Flask app
        app.app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False, threaded=True)
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        print("\nMake sure:")
        print("  1. backend/app.py exists")
        print("  2. All dependencies are installed")
        print("  3. .env file is configured")
        sys.exit(1)

def main():
    """Main entry point"""
    print("""
    ╔════════════════════════════════════════════════╗
    ║   🌟 Stellar Compass Desktop App 🌟          ║
    ╚════════════════════════════════════════════════╝
    """)
    
    print("🚀 Starting application...")
    
    # Check if backend folder exists
    backend_folder = Path(__file__).parent / 'backend'
    if not backend_folder.exists():
        print("❌ Error: backend folder not found!")
        print(f"   Expected location: {backend_folder}")
        sys.exit(1)
    
    # Check if app.py exists
    app_file = backend_folder / 'app.py'
    if not app_file.exists():
        print("❌ Error: backend/app.py not found!")
        print(f"   Expected location: {app_file}")
        sys.exit(1)
    
    # Start Flask in background
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    
    # Wait for server to start
    print("⏳ Initializing backend...")
    time.sleep(3)
    
    # Open in browser (app mode)
    print("🌐 Opening application window...")
    
    # Try Chrome app mode first (cleanest)
    chrome_path = None
    possible_chrome_paths = [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        os.path.expanduser(r'~\AppData\Local\Google\Chrome\Application\chrome.exe'),
    ]
    
    for path in possible_chrome_paths:
        if os.path.exists(path):
            chrome_path = path
            break
    
    # Determine the URL based on your current setup
    url = 'http://127.0.0.1:5000'
    
    # Check if you have a frontend folder serving on port 8080
    frontend_folder = Path(__file__).parent / 'frontend'
    if frontend_folder.exists():
        # If you have separate frontend, might need port 8080
        # But app.py should serve it on 5000 if configured correctly
        print(f"📁 Frontend folder found: {frontend_folder}")
    
    if chrome_path:
        # Open in app mode (no address bar, looks like desktop app)
        os.system(f'start "" "{chrome_path}" --app={url} --window-size=1200,800 --disable-web-security --user-data-dir="%TEMP%\\stellar-compass"')
        print("✅ Application opened in Chrome app mode")
    else:
        # Fallback to default browser
        webbrowser.open(url)
        print("✅ Application opened in browser")
        print("💡 Tip: Install Chrome for the best desktop app experience")
    
    print("\n" + "=" * 50)
    print("✅ Stellar Compass is running!")
    print("=" * 50)
    print("\n📝 Instructions:")
    print("   • Your app is now open in a window")
    print("   • Keep this console window open")
    print("   • Close this window to stop the app")
    print(f"\n🌐 URL: {url}")
    print("\nPress Ctrl+C to quit\n")
    
    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 Closing Stellar Compass... Goodbye!")
        sys.exit(0)

if __name__ == '__main__':
    main()