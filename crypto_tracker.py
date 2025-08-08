import requests
import json
from web3 import Web3
from datetime import datetime
import time

class CryptoTracker:
    def __init__(self):
        # Initialize Web3 for Ethereum
        self.w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161'))
        
        # API endpoints
        self.blockchain_info_url = "https://blockchain.info/rawaddr/"
        self.etherscan_url = "https://api.etherscan.io/api"
        self.etherscan_api_key = "YourEtherscanAPIKey"  # Get from https://etherscan.io/apis
        
    def get_bitcoin_balance(self, address):
        """Get Bitcoin address balance"""
        try:
            url = f"{self.blockchain_info_url}{address}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                balance_btc = data['final_balance'] / 100000000  # Convert satoshis to BTC
                return {
                    'address': address,
                    'balance_btc': balance_btc,
                    'total_received': data['total_received'] / 100000000,
                    'total_sent': data['total_sent'] / 100000000,
                    'n_tx': data['n_tx']
                }
            else:
                return None
        except Exception as e:
            print(f"Error getting Bitcoin balance for {address}: {e}")
            return None
    
    def get_ethereum_balance(self, address):
        """Get Ethereum address balance"""
        try:
            # Get ETH balance
            balance_wei = self.w3.eth.get_balance(address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            
            # Get ERC-20 token balances (example with USDT)
            usdt_contract = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
            usdt_abi = [
                {
                    "constant": True,
                    "inputs": [{"name": "_owner", "type": "address"}],
                    "name": "balanceOf",
                    "outputs": [{"name": "balance", "type": "uint256"}],
                    "type": "function"
                }
            ]
            
            try:
                contract = self.w3.eth.contract(address=usdt_contract, abi=usdt_abi)
                usdt_balance = contract.functions.balanceOf(address).call()
                usdt_balance_formatted = usdt_balance / 10**6  # USDT has 6 decimals
            except:
                usdt_balance_formatted = 0
            
            return {
                'address': address,
                'balance_eth': float(balance_eth),
                'balance_usdt': usdt_balance_formatted,
                'balance_wei': balance_wei
            }
        except Exception as e:
            print(f"Error getting Ethereum balance for {address}: {e}")
            return None
    
    def get_crypto_prices(self):
        """Get current crypto prices from CoinGecko"""
        try:
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                'ids': 'bitcoin,ethereum',
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_market_cap': 'true'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'bitcoin': {
                        'price': data['bitcoin']['usd'],
                        'change_24h': data['bitcoin']['usd_24h_change'],
                        'market_cap': data['bitcoin']['usd_market_cap']
                    },
                    'ethereum': {
                        'price': data['ethereum']['usd'],
                        'change_24h': data['ethereum']['usd_24h_change'],
                        'market_cap': data['ethereum']['usd_market_cap']
                    }
                }
            else:
                return None
        except Exception as e:
            print(f"Error getting crypto prices: {e}")
            return None
    
    def calculate_portfolio_value(self, addresses, prices):
        """Calculate total portfolio value"""
        total_value = 0
        portfolio_breakdown = {
            'bitcoin': {'balance': 0, 'value': 0},
            'ethereum': {'balance': 0, 'value': 0}
        }
        
        # Calculate Bitcoin portfolio
        for addr in addresses.get('bitcoin', []):
            btc_data = self.get_bitcoin_balance(addr)
            if btc_data:
                portfolio_breakdown['bitcoin']['balance'] += btc_data['balance_btc']
        
        # Calculate Ethereum portfolio
        for addr in addresses.get('ethereum', []):
            eth_data = self.get_ethereum_balance(addr)
            if eth_data:
                portfolio_breakdown['ethereum']['balance'] += eth_data['balance_eth']
        
        # Calculate USD values
        if prices:
            portfolio_breakdown['bitcoin']['value'] = (
                portfolio_breakdown['bitcoin']['balance'] * prices['bitcoin']['price']
            )
            portfolio_breakdown['ethereum']['value'] = (
                portfolio_breakdown['ethereum']['balance'] * prices['ethereum']['price']
            )
            
            total_value = (
                portfolio_breakdown['bitcoin']['value'] + 
                portfolio_breakdown['ethereum']['value']
            )
        
        return {
            'total_value': total_value,
            'breakdown': portfolio_breakdown,
            'prices': prices
        }
    
    def get_address_transactions(self, address, crypto_type='bitcoin'):
        """Get recent transactions for an address"""
        try:
            if crypto_type == 'bitcoin':
                url = f"{self.blockchain_info_url}{address}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get('txs', [])[:10]  # Last 10 transactions
            elif crypto_type == 'ethereum':
                # For Ethereum, you'd need to use Etherscan API
                # This is a simplified version
                return []
                
        except Exception as e:
            print(f"Error getting transactions for {address}: {e}")
            return []

# Example usage
if __name__ == "__main__":
    tracker = CryptoTracker()
    
    # Sample addresses
    addresses = {
        'bitcoin': [
            '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',  # Genesis block address
            '3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy'   # Another sample address
        ],
        'ethereum': [
            '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6',
            '0x1234567890123456789012345678901234567890'
        ]
    }
    
    # Get prices
    prices = tracker.get_crypto_prices()
    print("Crypto Prices:", prices)
    
    # Calculate portfolio value
    portfolio = tracker.calculate_portfolio_value(addresses, prices)
    print("Portfolio Value:", portfolio)
