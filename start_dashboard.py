#!/usr/bin/env python3
"""
🚀 Crypto Dashboard - All-in-One Startup Script
Handles everything from installation to launching the dashboard
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def print_banner():
    """Print startup banner"""
    print("=" * 60)
    print("🚀 CRYPTO PORTFOLIO DASHBOARD")
    print("=" * 60)
    print("📊 Real-time Bitcoin & Ethereum Tracking")
    print("🌙 Dark Theme Dashboard")
    print("📈 Interactive Charts & Analytics")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("📝 Creating configuration file...")
        
        env_content = """# Crypto Dashboard Configuration

# Flask Settings
SECRET_KEY=crypto-dashboard-secret-key-2024
DEBUG=True

# API Keys (Optional - Get from respective services)
ETHERSCAN_API_KEY=YourEtherscanAPIKey
INFURA_PROJECT_ID=9aa3d95b3bc440fa88ea12eaa4456161

# Add your real crypto addresses here (replace with your addresses)
# BITCOIN_ADDRESSES=address1,address2,address3
# ETHEREUM_ADDRESSES=address1,address2,address3

# Dashboard Settings
UPDATE_INTERVAL=30000
CHART_DAYS=365
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ Configuration file created")
        print("💡 Edit .env file to add your real addresses and API keys")
        return False
    else:
        print("✅ Configuration file already exists")
        return True

def check_port_available(port=8050):
    """Check if port is available"""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def start_dashboard():
    """Start the crypto dashboard"""
    print("\n🎯 Starting Crypto Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:8050")
    print("🔄 Auto-refresh every 30 seconds")
    print("⏹️  Press Ctrl+C to stop")
    print("\n" + "=" * 60)
    
    # Check if port is available
    if not check_port_available():
        print("❌ Port 8050 is already in use")
        print("💡 Please stop any other applications using port 8050")
        return False
    
    try:
        # Import and run the dashboard
        from app_enhanced import app, server
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(3)
            try:
                webbrowser.open('http://localhost:8050')
                print("🌐 Browser opened automatically")
            except:
                print("💡 Please open your browser to: http://localhost:8050")
        
        # Start browser in background
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Start the dashboard
        app.run_server(debug=False, host='0.0.0.0', port=8050)
        
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main startup function"""
    print_banner()
    
    # Check if we're in the right directory
    if not Path('app_enhanced.py').exists():
        print("❌ Please run this script from the projet_ia directory")
        print("💡 Navigate to the projet_ia folder and try again")
        return
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return
    
    # Create configuration file
    env_ready = create_env_file()
    
    # Start dashboard
    if start_dashboard():
        print("✅ Dashboard started successfully!")
    else:
        print("❌ Failed to start dashboard")

if __name__ == '__main__':
    main()
