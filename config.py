"""
Configuration file for SPX Bull Put Credit Spread Trading Bot
Customize these settings based on your preferences and risk tolerance
"""

import os
from datetime import time

class TradingConfig:
    """Main configuration class for the trading bot"""

    # Strategy Parameters
    RSI_THRESHOLD = 35          # Enter trades when RSI is below this level
    RSI_PERIOD = 14            # Number of periods for RSI calculation
    DAYS_TO_EXPIRY = 14        # Target days to expiration for options
    TARGET_DELTA = 0.5         # Target delta for short put (50 delta)
    SPREAD_WIDTH = 10          # Width of the spread in points
    PROFIT_TARGET = 0.5        # Profit target as percentage (50%)
    POSITION_SIZE = 1          # Number of contracts per trade

    # Risk Management
    MAX_POSITIONS = 5          # Maximum number of concurrent positions
    MIN_DTE = 7               # Minimum days to expiry before force close
    MAX_RISK_PER_TRADE = 1000  # Maximum risk per trade in dollars
    MAX_PORTFOLIO_RISK = 5000  # Maximum total portfolio risk

    # Trading Hours (EST)
    MARKET_OPEN = time(9, 30)
    MARKET_CLOSE = time(16, 0)

    # Platform Settings
    PREFERRED_PLATFORM = "IB"   # Options: "IB", "TDA", "ALPACA"
    USE_PAPER_TRADING = True    # Set to False for live trading

    # Interactive Brokers Settings
    IB_HOST = "127.0.0.1"
    IB_PAPER_PORT = 7497       # Paper trading port
    IB_LIVE_PORT = 7496        # Live trading port
    IB_CLIENT_ID = 1

    # TD Ameritrade Settings (if using TDA)
    TDA_API_KEY = os.getenv("TDA_API_KEY", "")
    TDA_REDIRECT_URI = os.getenv("TDA_REDIRECT_URI", "")
    TDA_REFRESH_TOKEN = os.getenv("TDA_REFRESH_TOKEN", "")

    # Alpaca Settings (if using Alpaca)
    ALPACA_PAPER_API_KEY = os.getenv("ALPACA_PAPER_API_KEY", "")
    ALPACA_PAPER_SECRET_KEY = os.getenv("ALPACA_PAPER_SECRET_KEY", "")
    ALPACA_LIVE_API_KEY = os.getenv("ALPACA_LIVE_API_KEY", "")
    ALPACA_LIVE_SECRET_KEY = os.getenv("ALPACA_LIVE_SECRET_KEY", "")

    # Data Sources
    DATA_SOURCE = "PRIMARY"     # Use primary platform for data
    BACKUP_DATA_SOURCE = "YAHOO"  # Fallback data source

    # Logging
    LOG_LEVEL = "INFO"         # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_TO_FILE = True
    LOG_FILE = "spx_bot.log"

    # Notifications (optional)
    ENABLE_EMAIL_ALERTS = False
    EMAIL_SMTP_SERVER = ""
    EMAIL_PORT = 587
    EMAIL_USERNAME = ""
    EMAIL_PASSWORD = ""
    EMAIL_RECIPIENTS = []

    # Telegram Notifications (optional)
    ENABLE_TELEGRAM = False
    TELEGRAM_BOT_TOKEN = ""
    TELEGRAM_CHAT_ID = ""

    # Backtesting
    BACKTEST_START_DATE = "2020-01-01"
    BACKTEST_END_DATE = "2025-01-01"
    INITIAL_CAPITAL = 100000

    # Order Management
    ORDER_TIMEOUT = 60         # Seconds to wait for order fill
    MAX_SLIPPAGE = 0.05       # Maximum acceptable slippage
    USE_LIMIT_ORDERS = True    # Use limit orders instead of market orders

    @classmethod
    def validate_config(cls):
        """Validate configuration settings"""
        errors = []

        # Validate required settings
        if cls.PREFERRED_PLATFORM not in ["IB", "TDA", "ALPACA"]:
            errors.append("PREFERRED_PLATFORM must be IB, TDA, or ALPACA")

        if cls.RSI_THRESHOLD <= 0 or cls.RSI_THRESHOLD >= 100:
            errors.append("RSI_THRESHOLD must be between 0 and 100")

        if cls.PROFIT_TARGET <= 0 or cls.PROFIT_TARGET >= 1:
            errors.append("PROFIT_TARGET must be between 0 and 1")

        if cls.POSITION_SIZE <= 0:
            errors.append("POSITION_SIZE must be greater than 0")

        # Platform-specific validation
        if cls.PREFERRED_PLATFORM == "TDA" and not cls.USE_PAPER_TRADING:
            if not cls.TDA_API_KEY or not cls.TDA_REFRESH_TOKEN:
                errors.append("TDA API credentials are required")

        if cls.PREFERRED_PLATFORM == "ALPACA":
            if cls.USE_PAPER_TRADING:
                if not cls.ALPACA_PAPER_API_KEY or not cls.ALPACA_PAPER_SECRET_KEY:
                    errors.append("Alpaca paper trading credentials are required")
            else:
                if not cls.ALPACA_LIVE_API_KEY or not cls.ALPACA_LIVE_SECRET_KEY:
                    errors.append("Alpaca live trading credentials are required")

        if errors:
            raise ValueError("Configuration errors:\n" + "\n".join(errors))

        return True

# Environment-specific configurations
class DevelopmentConfig(TradingConfig):
    """Development environment configuration"""
    USE_PAPER_TRADING = True
    LOG_LEVEL = "DEBUG"
    MAX_POSITIONS = 2
    POSITION_SIZE = 1

class ProductionConfig(TradingConfig):
    """Production environment configuration"""
    USE_PAPER_TRADING = False
    LOG_LEVEL = "INFO"
    ENABLE_EMAIL_ALERTS = True
    ORDER_TIMEOUT = 30

# Select configuration based on environment
ENV = os.getenv("TRADING_ENV", "development")
if ENV.lower() == "production":
    Config = ProductionConfig
else:
    Config = DevelopmentConfig
