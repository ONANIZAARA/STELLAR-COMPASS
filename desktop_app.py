"""
Stellar Compass - Windows Desktop Application
Main entry point for the desktop app
"""

import webview
import threading
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_path))

# Import Flask app
from backend.app import app

class StellarCompassApp:
    def __init__(self):
        self.window = None
        self.server_thread = None
        
    def start_flask(self):
        """Start Flask server in a separate thread"""
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
    
    def on_closing(self):
        """Handle window closing"""
        print("Closing Stellar Compass...")
        # Shutdown Flask server
        os._exit(0)
    
    def run(self):
        """Run the desktop application"""
        
        # Start Flask server in background thread
        self.server_thread = threading.Thread(target=self.start_flask, daemon=True)
        self.server_thread.start()
        
        # Wait a moment for Flask to start
        import time
        time.sleep(2)
        
        # Create desktop window
        self.window = webview.create_window(
            title='Stellar Compass - DeFi Assistant',
            url='http://127.0.0.1:5000',
            width=1200,
            height=800,
            resizable=True,
            fullscreen=False,
            min_size=(800, 600),
            background_color='#667eea',
            text_select=True
        )
        
        # Set window events
        self.window.events.closing += self.on_closing
        
        # Start the window
        webview.start(debug=False)

def main():
    """Main entry point"""
    print("🚀 Starting Stellar Compass Desktop App...")
    app_instance = StellarCompassApp()
    app_instance.run()

if __name__ == '__main__':
    main()
