# 🚀 Crypto Portfolio Dashboard

A modern, dark-themed dashboard for tracking Bitcoin and Ethereum addresses with real-time price data, interactive charts, and portfolio analytics.

## ✨ Features

- **Real-time Price Tracking**: Live Bitcoin and Ethereum prices from CoinGecko API
- **Interactive Charts**: Portfolio performance, price history, market cap distribution, and volume analysis
- **Address Tracking**: Monitor multiple Bitcoin and Ethereum addresses
- **Dark Theme**: Modern, eye-friendly dark interface
- **Auto-refresh**: Updates every 30 seconds
- **Responsive Design**: Works on desktop and mobile devices
- **Portfolio Analytics**: Track total portfolio value and individual holdings

## 📊 Dashboard Components

### Price Cards
- Current Bitcoin and Ethereum prices
- 24-hour price changes
- Market capitalization

### Charts & Analytics
1. **Portfolio Performance Chart**: Shows portfolio value over time
2. **Price History Chart**: Bitcoin and Ethereum price trends
3. **Market Cap Distribution**: Pie chart showing market cap allocation
4. **24h Volume Comparison**: Trading volume analysis

### Address Tracking
- Real-time balance checking for Bitcoin addresses
- Ethereum address monitoring with ETH and ERC-20 token balances
- Transaction history (coming soon)

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or navigate to the project directory**
   ```bash
   cd projet_ia
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create environment configuration**
   ```bash
   python config.py
   ```

4. **Edit the .env file** (created by step 3)
   - Add your Etherscan API key (get from https://etherscan.io/apis)
   - Add your real Bitcoin and Ethereum addresses
   - Customize other settings as needed

5. **Run the dashboard**
   ```bash
   python app_enhanced.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8050`

## 🔧 Configuration

### API Keys Required

1. **Etherscan API Key** (optional but recommended)
   - Get from: https://etherscan.io/apis
   - Used for detailed Ethereum address tracking

2. **Infura Project ID** (included)
   - Free tier available at: https://infura.io/
   - Used for Ethereum blockchain interactions

### Adding Your Addresses

Edit the `.env` file or modify `config.py`:

```python
BITCOIN_ADDRESSES = [
    'your-bitcoin-address-1',
    'your-bitcoin-address-2'
]

ETHEREUM_ADDRESSES = [
    'your-ethereum-address-1',
    'your-ethereum-address-2'
]
```

## 📈 Features in Detail

### Real-time Data
- **CoinGecko API**: Free, reliable crypto price data
- **Blockchain.info**: Bitcoin address balance checking
- **Web3.py**: Ethereum blockchain integration

### Charts & Visualization
- **Plotly**: Interactive, responsive charts
- **Dark Theme**: Optimized for extended viewing
- **Real-time Updates**: Auto-refresh every 30 seconds

### Security Features
- Environment variable configuration
- API key management
- No sensitive data in code

## 🚀 Usage

### Basic Usage
1. Start the application: `python app_enhanced.py`
2. Open browser to `http://localhost:8050`
3. View your portfolio dashboard

### Customization
- Edit `config.py` to change colors, intervals, and settings
- Modify `crypto_tracker.py` to add more cryptocurrencies
- Update address lists in the configuration

### API Endpoints
- `/`: Main dashboard
- `/api/crypto-data`: JSON crypto price data
- `/api/addresses`: JSON address information

## 🔮 Future Enhancements

- [ ] Transaction history tracking
- [ ] More cryptocurrencies (Cardano, Solana, etc.)
- [ ] Price alerts and notifications
- [ ] Export portfolio data
- [ ] Advanced analytics and predictions
- [ ] Mobile app version
- [ ] User authentication
- [ ] Multiple portfolio support

## 🛡️ Security Notes

- Never commit API keys to version control
- Use environment variables for sensitive data
- Consider using a VPN for additional security
- Regularly update dependencies

## 📝 Troubleshooting

### Common Issues

1. **Module not found errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **API rate limiting**
   - CoinGecko has generous free limits
   - Consider upgrading API keys for production use

3. **Address not found**
   - Verify address format is correct
   - Check if address has any balance

4. **Charts not loading**
   - Check internet connection
   - Verify Plotly is installed correctly

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- CoinGecko for free crypto price data
- Plotly for interactive charts
- Dash for the web framework
- Bootstrap for the dark theme

---

**Happy Crypto Tracking! 🚀📈**
