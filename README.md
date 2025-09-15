# SPX Bull Put Credit Spread Trading Bot Setup Guide

## Overview
This bot implements the SPX Bull Put Credit Spread strategy with 90% win rate based on RSI signals. It automatically:
- Monitors RSI levels on SPX
- Enters bull put spreads when RSI < 35
- Manages positions with 50% profit targets
- Supports multiple trading platforms

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Choose Your Platform

#### Option A: Interactive Brokers (Recommended)
- **Pros**: Best options data, reliable API, SPX support
- **Cons**: Requires TWS/IB Gateway running
- **Cost**: $1-10/month depending on data subscriptions

**Setup Steps:**
1. Open IB account at https://www.interactivebrokers.com/
2. Download and install TWS or IB Gateway
3. Enable API in TWS: Configure → API → Settings → Enable ActiveX and Socket Clients
4. Set Socket Port: 7497 (paper) or 7496 (live)
5. Run the bot!

#### Option B: TD Ameritrade/Schwab
- **Pros**: Good options support, established platform
- **Cons**: API being phased out, complex authentication
- **Cost**: Free with funded account

**Setup Steps:**
1. Open TD Ameritrade account
2. Apply for API access at https://developer.tdameritrade.com/
3. Get API key and set up OAuth
4. Configure credentials in .env file

#### Option C: Alpaca
- **Pros**: Clean API, good documentation
- **Cons**: Limited options support, no SPX (use SPY)
- **Cost**: Free paper trading

**Setup Steps:**
1. Sign up at https://alpaca.markets/
2. Get API keys from dashboard
3. Configure credentials in .env file

### 3. Configure Environment Variables

Create a `.env` file in the project directory:

```
# Choose your platform
TRADING_ENV=development
PREFERRED_PLATFORM=IB

# Interactive Brokers
IB_HOST=127.0.0.1
IB_PAPER_PORT=7497
IB_LIVE_PORT=7496

# TD Ameritrade (if using)
TDA_API_KEY=your_api_key_here
TDA_REFRESH_TOKEN=your_refresh_token_here
TDA_REDIRECT_URI=https://localhost

# Alpaca (if using)
ALPACA_PAPER_API_KEY=your_paper_key_here
ALPACA_PAPER_SECRET_KEY=your_paper_secret_here
ALPACA_LIVE_API_KEY=your_live_key_here
ALPACA_LIVE_SECRET_KEY=your_live_secret_here

# Optional: Notifications
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### 4. Paper Trading Setup

**Interactive Brokers:**
1. In TWS, go to Account → Market Data Subscriptions
2. Subscribe to "US Equity and Options Add-On Streaming Bundle" (free for paper)
3. Restart TWS
4. Set Socket Port to 7497 for paper trading
5. Run bot with USE_PAPER_TRADING=True

**TD Ameritrade:**
1. Paper trading is automatic with API access
2. No additional setup required

**Alpaca:**
1. Paper trading keys are separate from live keys
2. Use ALPACA_PAPER_* environment variables

### 5. Run the Bot

```bash
python spx_bull_put_bot.py
```

## Platform-Specific Detailed Setup

### Interactive Brokers Detailed Setup

#### Prerequisites
- Windows, Mac, or Linux computer
- Stable internet connection
- IB account with options trading permissions

#### Step-by-step IB Setup:

1. **Account Setup**
   - Open account at https://www.interactivebrokers.com/
   - Fund account (minimum $25,000 for portfolio margin recommended)
   - Apply for options trading permissions (Level 2 minimum)
   - Apply for index options trading permissions

2. **Software Installation**
   - Download TWS (Trader Workstation) or IB Gateway
   - Install and create shortcuts
   - Log in with your credentials

3. **API Configuration**
   - Open TWS
   - Go to File → Global Configuration → API → Settings
   - Check "Enable ActiveX and Socket Clients"
   - Set Socket Port: 7497 (paper) or 7496 (live)
   - Set Master API client ID: 0
   - Check "Allow connections from localhost only" for security
   - Click OK and restart TWS

4. **Market Data Setup**
   - Go to Account → Market Data Subscriptions
   - Subscribe to required data feeds:
     - US Securities Snapshot and Futures Value Bundle (free)
     - US Equity and Options Add-On Streaming Bundle (free for paper)
   - For live trading, consider:
     - OPRA (Options Price Reporting Authority)
     - CBOE index options data

5. **Test Connection**
   ```python
   from ib_insync import *
   ib = IB()
   ib.connect('127.0.0.1', 7497, clientId=1)
   print("Connection successful!" if ib.isConnected() else "Connection failed!")
   ```

### TD Ameritrade Detailed Setup

#### API Access Application
1. Go to https://developer.tdameritrade.com/
2. Sign up for developer account
3. Create new app:
   - App Name: "SPX Trading Bot"
   - Redirect URI: https://localhost
   - Purpose: Personal use

#### Authentication Setup
```python
# First time setup
import tda
from tda import auth

token_path = 'ameritrade-credentials.json'
api_key = 'YOUR_API_KEY@AMER.OAUTHAP'
redirect_uri = 'https://localhost'

try:
    c = auth.client_from_token_file(token_path, api_key)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome() as driver:
        c = auth.client_from_login_flow(
            driver, api_key, redirect_uri, token_path)
```

### Alpaca Detailed Setup

#### Account Setup
1. Sign up at https://alpaca.markets/
2. Complete identity verification
3. Fund account (optional for paper trading)

#### API Keys
1. Go to dashboard
2. Navigate to API section
3. Generate paper trading keys
4. Generate live trading keys (when ready)

#### Test Connection
```python
from alpaca.trading.client import TradingClient

trading_client = TradingClient(
    api_key='YOUR_API_KEY',
    secret_key='YOUR_SECRET_KEY',
    paper=True
)

account = trading_client.get_account()
print(f"Account: {account.account_number}")
print(f"Buying Power: ${account.buying_power}")
```

## Strategy Customization

### Risk Management Parameters
Edit `config.py` to adjust:
- `RSI_THRESHOLD`: Entry signal level (default: 35)
- `PROFIT_TARGET`: Exit target percentage (default: 50%)
- `MAX_POSITIONS`: Maximum concurrent trades (default: 5)
- `POSITION_SIZE`: Contracts per trade (default: 1)
- `MAX_RISK_PER_TRADE`: Maximum loss per trade (default: $1000)

### Advanced Settings
- `DAYS_TO_EXPIRY`: Target DTE for options (default: 14)
- `SPREAD_WIDTH`: Strike price difference (default: 10)
- `MIN_DTE`: Force close before expiration (default: 7)

## Troubleshooting

### Common Issues

1. **"Connection refused" error**
   - Ensure TWS/IB Gateway is running
   - Check API is enabled in TWS settings
   - Verify correct port (7497 for paper, 7496 for live)

2. **"No market data" error**
   - Subscribe to required market data in TWS
   - Check Account → Market Data Subscriptions
   - Restart TWS after adding subscriptions

3. **"Contract not found" error**
   - Verify SPX options permissions
   - Check exchange settings (use 'SMART' for IB)
   - Ensure options chain has sufficient liquidity

4. **Import errors**
   - Run: `pip install -r requirements.txt`
   - For TA-Lib issues on Windows: `conda install -c conda-forge ta-lib`

5. **Permission denied for options trading**
   - Apply for options permissions in your broker account
   - Wait for approval (can take 1-3 business days)
   - Check account requirements (minimum balance, experience)

### Getting Help

1. **Interactive Brokers**: 
   - API Documentation: https://interactivebrokers.github.io/tws-api/
   - Support: Chat or phone support available 24/5

2. **TD Ameritrade/Schwab**:
   - Developer Forum: https://developer.tdameritrade.com/community
   - Documentation: https://tda-api.readthedocs.io/

3. **Alpaca**:
   - Documentation: https://alpaca.markets/docs/
   - Community: https://forum.alpaca.markets/

## Risk Disclosure

**IMPORTANT**: This bot trades options, which involve substantial risk. You can lose more than your initial investment. Key risks include:

- **Market Risk**: Markets can move against your positions
- **Volatility Risk**: High volatility can cause large losses
- **Liquidity Risk**: Options may be difficult to close
- **Assignment Risk**: Short options may be assigned early
- **Technology Risk**: API failures or bot errors can cause losses

**Recommendations**:
- Start with paper trading
- Use small position sizes initially
- Monitor the bot actively
- Understand the strategy thoroughly
- Never invest more than you can afford to lose

## Next Steps

1. **Paper Trade First**: Run the bot in paper trading mode for at least 2-4 weeks
2. **Monitor Performance**: Track win rate, profit/loss, and maximum drawdown
3. **Optimize Settings**: Adjust parameters based on market conditions
4. **Scale Gradually**: Start with 1 contract, increase as you gain confidence
5. **Stay Informed**: Monitor market news and volatility events

## Legal Disclaimer

This software is for educational purposes only. The authors are not financial advisors and make no investment recommendations. Trading options involves substantial risk and may not be suitable for all investors. Past performance does not guarantee future results.
