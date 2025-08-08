import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # API Keys (get these from respective services)
    ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY', 'YourEtherscanAPIKey')
    INFURA_PROJECT_ID = os.getenv('INFURA_PROJECT_ID', '9aa3d95b3bc440fa88ea12eaa4456161')
    
    # Crypto addresses to track (replace with your real addresses)
    BITCOIN_ADDRESSES = [
        '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',  # Genesis block address (sample)
        '3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy'   # Another sample address
    ]
    
    ETHEREUM_ADDRESSES = [
        '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6',  # Sample address
        '0x1234567890123456789012345678901234567890'     # Another sample address
    ]
    
    # Dashboard settings
    UPDATE_INTERVAL = 30000  # 30 seconds
    CHART_DAYS = 365  # Number of days for historical charts
    
    # API endpoints
    COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"
    BLOCKCHAIN_INFO_URL = "https://blockchain.info/rawaddr/"
    ETHERSCAN_URL = "https://api.etherscan.io/api"
    
    # Web3 provider
    WEB3_PROVIDER = f"https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}"
    
    # Chart colors
    CHART_COLORS = {
        'bitcoin': '#f7931a',
        'ethereum': '#627eea',
        'portfolio': '#00ff88',
        'success': '#28a745',
        'warning': '#ffc107',
        'danger': '#dc3545',
        'info': '#17a2b8'
    }
    
    # Sample portfolio data (replace with real data)
    SAMPLE_PORTFOLIO = {
        'bitcoin': {
            'holdings': 0.5,  # BTC
            'addresses': BITCOIN_ADDRESSES
        },
        'ethereum': {
            'holdings': 2.5,  # ETH
            'addresses': ETHEREUM_ADDRESSES
        }
    }

# Create .env file template
def create_env_template():
    """Create a .env template file"""
    env_template = """# Crypto Dashboard Configuration

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
        f.write(env_template)
    
    print("Created .env template file. Please edit it with your real API keys and addresses.")

if __name__ == "__main__":
    create_env_template()
