#!/usr/bin/env python3
"""
Crypto Dashboard Startup Script
Handles initial setup and launches the dashboard
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask', 'dash', 'plotly', 'pandas', 'requests', 
        'dash-bootstrap-components', 'python-dotenv', 'web3'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Installing dependencies...")
        
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please run:")
            print("   pip install -r requirements.txt")
            return False
    
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("📝 Creating .env configuration file...")
        
        env_content = """# Crypto Dashboard Configuration

# Flask Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# API Keys (Get these from respective services)
ETHERSCAN_API_KEY=YourEtherscanAPIKey
INFURA_PROJECT_ID=9aa3d95b3bc440fa88ea12eaa4456161

# Add your real crypto addresses here
# BITCOIN_ADDRESSES=address1,address2,address3
# ETHEREUM_ADDRESSES=address1,address2,address3

# Dashboard Settings
UPDATE_INTERVAL=30000
CHART_DAYS=365
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ Created .env file")
        print("📝 Please edit .env file with your real API keys and addresses")
        return False
    else:
        return True

def main():
    """Main startup function"""
    print("🚀 Crypto Portfolio Dashboard")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path('app_enhanced.py').exists():
        print("❌ Please run this script from the projet_ia directory")
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Create .env file if needed
    env_ready = create_env_file()
    
    print("\n🎯 Starting Crypto Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:8050")
    print("🔄 Auto-refresh every 30 seconds")
    print("⏹️  Press Ctrl+C to stop")
    print("\n" + "=" * 40)
    
    try:
        # Import and run the dashboard
        from app_enhanced import app, server
        
        if __name__ == '__main__':
            app.run_server(debug=True, host='0.0.0.0', port=8050)
    
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")

if __name__ == '__main__':
    main()
