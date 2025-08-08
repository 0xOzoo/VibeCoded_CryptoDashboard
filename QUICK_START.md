# 🚀 Quick Start Guide

## **One-Click Startup**

### **Option 1: Windows Batch File (Recommended)**
```bash
# Simply double-click this file:
start.bat
```

### **Option 2: Python Script**
```bash
python start_dashboard.py
```

## **What the Startup Script Does:**

1. ✅ **Checks Python version** (requires 3.8+)
2. 📦 **Installs dependencies** automatically
3. 📝 **Creates configuration file** (.env)
4. 🌐 **Opens browser** to dashboard
5. 🚀 **Starts the dashboard** on http://localhost:8050

## **Dashboard Features:**

- 📊 **Real-time crypto prices** (Bitcoin & Ethereum)
- 📈 **Interactive charts** and analytics
- 💼 **Portfolio tracking** with address monitoring
- 🌙 **Dark theme** interface
- 🔄 **Auto-refresh** every 30 seconds

## **Customization:**

### **Add Your Real Addresses:**
Edit the `.env` file and add your addresses:
```
BITCOIN_ADDRESSES=your-bitcoin-address-1,your-bitcoin-address-2
ETHEREUM_ADDRESSES=your-ethereum-address-1,your-ethereum-address-2
```

### **Get API Keys (Optional):**
- **Etherscan API**: https://etherscan.io/apis
- **Infura Project ID**: https://infura.io/

## **Troubleshooting:**

### **Port Already in Use:**
```bash
# Find what's using port 8050
netstat -ano | findstr :8050

# Kill the process
taskkill /PID <process_id> /F
```

### **Python Not Found:**
- Download Python from: https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### **Dependencies Error:**
```bash
pip install -r requirements.txt
```

## **Stop the Dashboard:**
- Press `Ctrl+C` in the terminal
- Or close the terminal window

---

**🎉 That's it! Your crypto dashboard is ready to use!**
